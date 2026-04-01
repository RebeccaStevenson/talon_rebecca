#!/usr/bin/env bash
set -euo pipefail

# Generic SuperWhisper mode switcher (macOS).
#
# Usage:
#   ./superwhisper_mode_template.sh normal
#   ./superwhisper_mode_template.sh local
#   ./superwhisper_mode_template.sh super
#
# Notes:
# - Uses SuperWhisper URL scheme via `open`.
# - `-g` avoids stealing focus.
# - If mode switching is unreliable, increase the sleep.

MODE_KEY="${1:-}"
if [[ -z "${MODE_KEY}" ]]; then
  echo "Usage: $0 <mode_key>" >&2
  exit 2
fi

/usr/bin/open -g "superwhisper://record"
sleep 0.15
/usr/bin/open -g "superwhisper://mode?key=${MODE_KEY}"

