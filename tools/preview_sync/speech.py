"""Speech-process control for preview sync."""

from __future__ import annotations

import os
import signal
import subprocess
import threading


class SpeechController:
    """Manage a single background macOS `say` process."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._proc: subprocess.Popen | None = None

    def get_proc(self) -> subprocess.Popen | None:
        with self._lock:
            if self._proc and self._proc.poll() is not None:
                self._proc = None
            return self._proc

    def is_speaking(self) -> bool:
        return self.get_proc() is not None

    def stop(self) -> None:
        with self._lock:
            proc = self._proc
            self._proc = None

        if not proc:
            return

        try:
            os.killpg(proc.pid, signal.SIGTERM)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass

    def start(self, sentence: str) -> None:
        if not sentence or not sentence.strip():
            raise ValueError("No sentence to speak")

        self.stop()

        proc = subprocess.Popen(
            ["say", sentence.strip()],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
            close_fds=True,
        )

        def _wait_for_speech() -> None:
            try:
                proc.wait()
            except Exception:
                pass
            finally:
                with self._lock:
                    if self._proc is proc:
                        self._proc = None

        with self._lock:
            self._proc = proc
        threading.Thread(target=_wait_for_speech, daemon=True).start()
