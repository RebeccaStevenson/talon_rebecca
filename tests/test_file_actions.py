"""Tests for file opening helpers."""

import sys

if "pytest" in sys.modules:
    import user.talon_rebecca.tools.files.file_actions as file_actions

    def test_open_file_custom_uses_macos_open(monkeypatch):
        calls = []

        monkeypatch.setattr(file_actions.app, "platform", "mac")
        monkeypatch.setattr(
            file_actions.subprocess,
            "run",
            lambda args, check=False: calls.append((args, check)),
        )

        file_actions.Actions.open_file_custom("/tmp/example.txt")

        assert calls == [(["open", "/tmp/example.txt"], False)]

    def test_open_file_custom_uses_windows_startfile(monkeypatch):
        calls = []

        monkeypatch.setattr(file_actions.app, "platform", "windows")
        monkeypatch.setattr(
            file_actions.os,
            "startfile",
            lambda path, operation="open": calls.append((path, operation)),
            raising=False,
        )

        file_actions.Actions.open_file_custom(r"C:\Temp\example.txt")

        assert calls == [(r"C:\Temp\example.txt", "open")]
