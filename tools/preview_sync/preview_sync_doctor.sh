#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
USER_DIR="$(cd "$REPO_DIR/.." && pwd)"
SERVER_SCRIPT="$SCRIPT_DIR/capture_server.py"
PRIVATE_ROOTS_CONFIG="$USER_DIR/talon_rebecca_private/settings/preview_sync_roots.json"
PUBLIC_ROOTS_CONFIG="$REPO_DIR/settings/preview_sync_roots.json"
if [[ -f "$PRIVATE_ROOTS_CONFIG" ]]; then
  ROOTS_CONFIG="$PRIVATE_ROOTS_CONFIG"
else
  ROOTS_CONFIG="$PUBLIC_ROOTS_CONFIG"
fi
SERVER_URL="http://127.0.0.1:27832"
SERVER_LOG="$SCRIPT_DIR/preview_sync.log"
DEBUG_DIR="$SCRIPT_DIR/debug"

COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_RED='\033[0;31m'
COLOR_RESET='\033[0m'

ok() { printf "${COLOR_GREEN}OK${COLOR_RESET} %s\n" "$*"; }
warn() { printf "${COLOR_YELLOW}WARN${COLOR_RESET} %s\n" "$*"; }
err() { printf "${COLOR_RED}ERR${COLOR_RESET} %s\n" "$*"; }

usage() {
  cat <<'EOF'
preview_sync_doctor.sh - automate preview_sync diagnostics and recovery

Usage:
  preview_sync_doctor.sh all [--source /path/to/file.md]
  preview_sync_doctor.sh health
  preview_sync_doctor.sh restart
  preview_sync_doctor.sh fix
  preview_sync_doctor.sh smoke
  preview_sync_doctor.sh debug
  preview_sync_doctor.sh notes-path --source /path/to/file.md
  preview_sync_doctor.sh capture-probe [--source /path/to/file.md]

Notes:
- all: runs fix + health + smoke + notes-path + capture-probe + debug
- capture-probe appends a test line to the resolved notes file
EOF
}

server_health() {
  curl -fsS "$SERVER_URL/health" >/dev/null 2>&1
}

ensure_server() {
  if server_health; then
    ok "capture server is healthy"
    return 0
  fi

  warn "capture server not healthy; starting $SERVER_SCRIPT"
  nohup python "$SERVER_SCRIPT" >/tmp/preview_sync_server.out 2>&1 &

  local i
  for i in 1 2 3 4 5 6 7 8 9 10; do
    sleep 0.2
    if server_health; then
      ok "capture server started"
      return 0
    fi
  done

  err "failed to start capture server"
  return 1
}

restart_server() {
  pkill -f 'tools/preview_sync/capture_server.py' >/dev/null 2>&1 || true
  sleep 0.2
  ensure_server
}

read_roots() {
  if [[ ! -f "$ROOTS_CONFIG" ]]; then
    warn "roots config missing at $ROOTS_CONFIG"
    return 1
  fi

  python - <<PY
import json
from pathlib import Path
cfg = Path(r'''$ROOTS_CONFIG''')
data = json.loads(cfg.read_text(encoding='utf-8'))
for item in data.get('roots', []):
    print(item)
PY
}

find_source_candidate() {
  local roots root candidate
  roots="$(read_roots || true)"
  while IFS= read -r root; do
    [[ -z "$root" ]] && continue
    if [[ ! -d "$root" ]]; then
      continue
    fi

    candidate="$(find "$root" -type f \( -name '*.md' -o -name '*.qmd' \) \
      ! -path '*/_notes/*' ! -name '*_notes.md' ! -name '*_citation.md' \
      -print0 2>/dev/null | xargs -0 ls -t 2>/dev/null | head -n 1 || true)"

    if [[ -n "$candidate" ]]; then
      echo "$candidate"
      return 0
    fi
  done <<< "$roots"

  return 1
}

notes_path_for_source() {
  local source="$1"
  local dir base stem
  dir="$(dirname "$source")"
  base="$(basename "$source")"
  stem="${base%.*}"
  stem="${stem%_notes}"
  stem="${stem%_citation}"
  printf '%s/%s_notes/%s_notes.md\n' "$dir" "$stem" "$stem"
}

run_health() {
  ensure_server || return 1

  local status
  status="$(curl -fsS "$SERVER_URL/speak_status" 2>/dev/null || true)"
  if [[ -n "$status" ]]; then
    ok "speak_status: $status"
  else
    warn "could not read /speak_status"
  fi

  if lsof -nP -iTCP:27832 -sTCP:LISTEN >/dev/null 2>&1; then
    ok "port 27832 is listening"
  else
    warn "port 27832 not detected as LISTEN"
  fi
}

run_fix() {
  ok "running fix: restart server, validate roots"
  restart_server || return 1

  local missing=0 root
  while IFS= read -r root; do
    [[ -z "$root" ]] && continue
    if [[ -d "$root" ]]; then
      ok "root exists: $root"
    else
      warn "root missing: $root"
      missing=$((missing + 1))
    fi
  done < <(read_roots || true)

  if [[ $missing -gt 0 ]]; then
    warn "one or more roots are missing; capture may fail"
  fi
}

run_smoke() {
  ok "running smoke checks"
  (
    cd "$REPO_DIR" || exit 1
    python -m py_compile tools/preview_sync/capture_server.py
    node --check tools/preview_sync/preview_sync_chrome_extension/content.js
    node --check tools/preview_sync/preview_sync_chrome_extension/background.js
    python -m pytest tests/test_preview_sync_capture_server.py -q
  )
  ok "smoke checks passed"
}

run_notes_path() {
  local source="$1"
  if [[ -z "$source" ]]; then
    if ! source="$(find_source_candidate)"; then
      warn "could not auto-detect source file"
      return 1
    fi
    warn "auto-detected source: $source"
  fi

  if [[ ! -f "$source" ]]; then
    err "source file not found: $source"
    return 1
  fi

  local notes
  notes="$(notes_path_for_source "$source")"
  if [[ -z "$notes" ]]; then
    err "failed to resolve notes path for source"
    return 1
  fi
  ok "source: $source"
  ok "notes : $notes"
}

run_capture_probe() {
  ensure_server || return 1

  local source="$1"
  if [[ -z "$source" ]]; then
    if ! source="$(find_source_candidate)"; then
      warn "capture probe skipped: no source file found"
      return 1
    fi
    warn "auto-detected source for probe: $source"
  fi

  if [[ ! -f "$source" ]]; then
    err "source file not found: $source"
    return 1
  fi

  local stem sentence notes_path payload resp
  stem="$(basename "$source")"
  stem="${stem%.*}"
  sentence="preview_sync_doctor probe $(date '+%Y-%m-%d %H:%M:%S')"
  notes_path="$(notes_path_for_source "$source")"
  if [[ -z "$notes_path" ]]; then
    err "failed to resolve notes path for source"
    return 1
  fi

  payload="$(cat <<JSON
{"sentence":"$sentence","pageUrl":"http://localhost:4444/","title":"$stem","sourceHints":["$stem"]}
JSON
)"

  resp="$(curl -fsS -X POST "$SERVER_URL/capture" -H 'Content-Type: application/json' -d "$payload" 2>/dev/null || true)"
  if [[ -z "$resp" ]]; then
    err "capture probe request failed"
    return 1
  fi
  ok "capture response: $resp"

  if [[ -f "$notes_path" ]] && rg -F "$sentence" "$notes_path" >/dev/null 2>&1; then
    ok "capture verified in notes file"
  else
    warn "capture response succeeded but probe sentence not found in expected notes file"
    warn "expected file: $notes_path"
    return 1
  fi
}

run_debug() {
  mkdir -p "$DEBUG_DIR"
  local out
  out="$DEBUG_DIR/preview_sync_debug_$(date '+%Y%m%d_%H%M%S').txt"

  {
    echo "# Preview Sync Debug Bundle"
    echo "Generated: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
    echo
    echo "## Paths"
    echo "Repo: $REPO_DIR"
    echo "Server script: $SERVER_SCRIPT"
    echo "Roots config: $ROOTS_CONFIG"
    echo "Server log: $SERVER_LOG"
    echo
    echo "## Health"
    if curl -fsS "$SERVER_URL/health"; then
      echo
    else
      echo "health endpoint unavailable"
    fi
    if curl -fsS "$SERVER_URL/speak_status"; then
      echo
    else
      echo "speak_status unavailable"
    fi
    echo
    echo "## Port 27832"
    lsof -nP -iTCP:27832 -sTCP:LISTEN || true
    echo
    echo "## Process"
    pgrep -fal 'tools/preview_sync/capture_server.py' || true
    echo
    echo "## Roots config"
    cat "$ROOTS_CONFIG" 2>/dev/null || true
    echo
    echo "## preview_sync.log (tail 120)"
    tail -n 120 "$SERVER_LOG" 2>/dev/null || true
    echo
    echo "## talon.log filtered (tail 160)"
    tail -n 2000 "$HOME/.talon/talon.log" 2>/dev/null | rg -n 'preview_sync|capture_server|ERROR|ActionProtoError|WARNING' | tail -n 160 || true
  } > "$out"

  ok "debug bundle written: $out"
}

main() {
  local cmd="${1:-all}"
  shift || true

  local source=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --source)
        source="${2:-}"
        shift 2
        ;;
      -h|--help)
        usage
        return 0
        ;;
      *)
        err "unknown arg: $1"
        usage
        return 2
        ;;
    esac
  done

  case "$cmd" in
    all)
      run_fix || return 1
      run_health || return 1
      run_smoke || return 1
      run_notes_path "$source" || true
      run_capture_probe "$source" || true
      run_debug || return 1
      ;;
    health)
      run_health
      ;;
    restart)
      restart_server
      ;;
    fix)
      run_fix
      ;;
    smoke)
      run_smoke
      ;;
    debug)
      run_debug
      ;;
    notes-path)
      run_notes_path "$source"
      ;;
    capture-probe)
      run_capture_probe "$source"
      ;;
    *)
      err "unknown command: $cmd"
      usage
      return 2
      ;;
  esac
}

main "$@"
