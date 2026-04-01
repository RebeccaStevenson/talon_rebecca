import os
import signal
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

from talon import Module, app, cron

mod = Module()

HOST = "127.0.0.1"
PORT = 27832
HEALTH_URL = f"http://{HOST}:{PORT}/health"
SERVER_SCRIPT = Path(__file__).resolve().parent / "capture_server.py"
PID_FILE = Path(__file__).resolve().parent / ".preview_sync_server.pid"
_SERVER_PROC: subprocess.Popen | None = None
_SERVER_POLL_JOB = None


def _poll_server_process() -> None:
    global _SERVER_PROC, _SERVER_POLL_JOB
    if _SERVER_PROC is not None and _SERVER_PROC.poll() is None:
        return

    _SERVER_PROC = None
    if _SERVER_POLL_JOB is not None:
        cron.cancel(_SERVER_POLL_JOB)
        _SERVER_POLL_JOB = None


def _healthcheck(timeout: float = 0.3) -> bool:
    try:
        with urllib.request.urlopen(HEALTH_URL, timeout=timeout) as response:
            return response.status == 200
    except (urllib.error.URLError, TimeoutError, ValueError, ConnectionError, OSError):
        return False
    except Exception:
        return False


def _read_pid() -> int | None:
    if not PID_FILE.exists():
        return None
    try:
        pid = int(PID_FILE.read_text(encoding="utf-8").strip())
    except Exception:
        return None
    return pid if pid > 0 else None


def _write_pid(pid: int):
    PID_FILE.write_text(str(pid), encoding="utf-8")


def _clear_pid():
    PID_FILE.unlink(missing_ok=True)


def _start():
    global _SERVER_PROC, _SERVER_POLL_JOB
    if _healthcheck():
        return

    proc = subprocess.Popen(
        [sys.executable, str(SERVER_SCRIPT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        close_fds=True,
    )
    _SERVER_PROC = proc
    if _SERVER_POLL_JOB is None:
        _SERVER_POLL_JOB = cron.interval("500ms", _poll_server_process)
    _write_pid(proc.pid)


def _stop():
    global _SERVER_PROC, _SERVER_POLL_JOB
    pid = _read_pid()
    if not pid:
        return

    try:
        os.killpg(pid, signal.SIGTERM)
    except Exception:
        try:
            os.kill(pid, signal.SIGTERM)
        except Exception:
            pass
    _SERVER_PROC = None
    if _SERVER_POLL_JOB is not None:
        cron.cancel(_SERVER_POLL_JOB)
        _SERVER_POLL_JOB = None
    _clear_pid()


@mod.action_class
class Actions:
    def preview_sync_server_start():
        """Start local preview sync capture server."""
        _start()

    def preview_sync_server_stop():
        """Stop local preview sync capture server."""
        _stop()

    def preview_sync_server_restart():
        """Restart local preview sync capture server."""
        _stop()
        _start()


# Ensure server is available shortly after Talon startup without blocking module load.
app.register("ready", lambda: _start())
