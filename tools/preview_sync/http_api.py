"""HTTP handler factory for preview sync."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse


def create_handler(api):
    """Build a request handler bound to the provided preview-sync API."""

    class Handler(BaseHTTPRequestHandler):
        def send_json(self, status: int, payload: dict) -> None:
            body = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()
            self.wfile.write(body)

        def do_OPTIONS(self) -> None:
            if not api.is_allowed_origin(self.headers.get("Origin")):
                self.send_json(403, {"ok": False, "error": "Origin not allowed"})
                return
            self.send_json(200, {"ok": True})

        def do_GET(self) -> None:
            if self.path == "/health":
                self.send_json(200, {"ok": True, "service": "preview-sync"})
                return

            if self.path == "/speak_status":
                self.send_json(200, {"ok": True, "speaking": api.is_speaking()})
                return

            if self.path.startswith("/pin_status"):
                parsed = urlparse(self.path)
                query = parse_qs(parsed.query or "")
                scope_raw = query.get("scope", [""])[0]
                scope = api.sanitize_scope(scope_raw, "")
                pinned = api.get_pinned_source(scope) if scope else None
                self.send_json(
                    200,
                    {
                        "ok": True,
                        "scope": scope,
                        "pinned": bool(pinned),
                        "sourcePath": str(pinned) if pinned else "",
                    },
                )
                return

            self.send_json(404, {"ok": False, "error": "Not found"})

        def do_POST(self) -> None:
            if not api.is_allowed_origin(self.headers.get("Origin")):
                self.send_json(403, {"ok": False, "error": "Origin not allowed"})
                return

            if self.path == "/speak":
                payload = _read_json_payload(self)
                if payload is None:
                    self.send_json(400, {"ok": False, "error": "Invalid JSON payload"})
                    return

                sentence = payload.get("sentence", "")
                try:
                    api.start_speaking(sentence)
                except api.error_class as exc:
                    self.send_json(422, {"ok": False, "error": str(exc)})
                    return
                except Exception as exc:
                    self.send_json(500, {"ok": False, "error": f"Speak failed: {exc}"})
                    return

                self.send_json(200, {"ok": True, "speaking": True})
                return

            if self.path == "/speak_stop":
                api.stop_speaking()
                self.send_json(200, {"ok": True, "speaking": False})
                return

            if self.path == "/pin_source":
                payload = _read_json_payload(self)
                if payload is None:
                    self.send_json(400, {"ok": False, "error": "Invalid JSON payload"})
                    return

                page_url = payload.get("pageUrl", "")
                source_hints = api.sanitize_source_hints(payload.get("sourceHints", []))
                scope = api.sanitize_scope(payload.get("scope", ""), page_url)

                try:
                    source_path = api.resolve_source(page_url, source_hints)
                except api.error_class as exc:
                    api.log_event(
                        "pin_error",
                        error=str(exc),
                        url=page_url,
                        hints="|".join(source_hints),
                        scope=scope,
                    )
                    self.send_json(422, {"ok": False, "error": str(exc)})
                    return
                except Exception as exc:
                    api.log_event(
                        "pin_error",
                        error=f"Pin failed: {exc}",
                        url=page_url,
                        hints="|".join(source_hints),
                        scope=scope,
                    )
                    self.send_json(500, {"ok": False, "error": f"Pin failed: {exc}"})
                    return

                api.set_pinned_source(scope, source_path)
                api.log_event("pin_set", scope=scope, source=source_path, url=page_url)
                self.send_json(
                    200,
                    {"ok": True, "scope": scope, "sourcePath": str(source_path)},
                )
                return

            if self.path == "/unpin_source":
                raw = _read_raw_body(self)
                scope = ""
                if raw:
                    try:
                        payload = json.loads(raw.decode("utf-8"))
                        scope = api.sanitize_scope(
                            payload.get("scope", ""),
                            payload.get("pageUrl", ""),
                        )
                    except Exception:
                        scope = ""

                if scope:
                    api.clear_pinned_source(scope)
                    api.log_event("pin_clear", scope=scope)
                else:
                    api.clear_pinned_source()
                    api.log_event("pin_clear_all")
                self.send_json(200, {"ok": True, "scope": scope})
                return

            if self.path != "/capture":
                self.send_json(404, {"ok": False, "error": "Not found"})
                return

            payload = _read_json_payload(self)
            if payload is None:
                self.send_json(400, {"ok": False, "error": "Invalid JSON payload"})
                return

            sentence = payload.get("sentence", "")
            page_url = payload.get("pageUrl", "")
            source_hints = api.sanitize_source_hints(payload.get("sourceHints", []))
            use_pinned = bool(payload.get("usePinned", True))
            scope = api.sanitize_scope(payload.get("scope", ""), page_url)
            pinned_source = api.get_pinned_source(scope) if use_pinned else None

            try:
                notes_path, source_path = api.append_capture(
                    sentence,
                    page_url,
                    source_hints,
                    pinned_source,
                )
            except api.error_class as exc:
                api.log_event(
                    "capture_error",
                    error=str(exc),
                    sentence_len=len(sentence or ""),
                    url=page_url,
                    hints="|".join(source_hints),
                    scope=scope,
                    use_pinned=use_pinned,
                )
                self.send_json(422, {"ok": False, "error": str(exc)})
                return
            except Exception as exc:
                api.log_event(
                    "capture_error",
                    error=f"Capture failed: {exc}",
                    sentence_len=len(sentence or ""),
                    url=page_url,
                    hints="|".join(source_hints),
                    scope=scope,
                    use_pinned=use_pinned,
                )
                self.send_json(500, {"ok": False, "error": f"Capture failed: {exc}"})
                return

            self.send_json(
                200,
                {
                    "ok": True,
                    "notesPath": str(notes_path),
                    "notesFile": notes_path.name,
                    "sourcePath": str(source_path),
                    "scope": scope,
                    "usedPinnedSource": bool(pinned_source),
                },
            )

        def log_message(self, format, *args) -> None:
            return

    return Handler


def _read_raw_body(handler: BaseHTTPRequestHandler) -> bytes:
    length = int(handler.headers.get("Content-Length", "0"))
    return handler.rfile.read(length)


def _read_json_payload(handler: BaseHTTPRequestHandler) -> dict | None:
    raw = _read_raw_body(handler)
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception:
        return None
