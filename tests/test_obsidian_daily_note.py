"""Tests for obsidian_daily_note helper functions."""

import os
import sys
import time

if "pytest" in sys.modules:
    import pytest

    import user.talon_rebecca.notes.daily_note_domain as domain
    import user.talon_rebecca.notes.note_config as note_config
    import user.talon_rebecca.notes.obsidian_daily_note as mod
    from talon import actions, app

    def setup_function():
        actions.reset_test_actions()
        app.notifications.clear()
        actions.register_test_action(
            "user", "audio_set_system_output_shokz", lambda: None
        )

    def test_daily_note_path_uses_configured_vault_dir(monkeypatch, tmp_path):
        config_path = tmp_path / "note_paths.json"
        vault_dir = tmp_path / "vault"
        config_path.write_text(
            '{"obsidian_vault_dir": "' + str(vault_dir) + '"}\n',
            encoding="utf-8",
        )
        monkeypatch.setattr(note_config, "_PRIVATE_NOTE_PATHS_CONFIG", config_path)
        monkeypatch.setattr(
            note_config, "_PUBLIC_NOTE_PATHS_CONFIG", tmp_path / "missing.json"
        )
        monkeypatch.setattr(mod, "_DAILY_DIR_OVERRIDE", None)

        path = mod._daily_note_path()

        assert path.parent == vault_dir / "daily"

    # -- _daily_note_path -------------------------------------------------

    def test_daily_note_path_uses_vault_dir(monkeypatch, tmp_path):
        monkeypatch.setattr(mod, "_DAILY_DIR_OVERRIDE", tmp_path)
        path = domain.daily_note_path(tmp_path)
        assert path.parent == tmp_path
        assert path.suffix == ".md"

    def test_daily_note_path_filename_is_iso_date(monkeypatch, tmp_path):
        from datetime import datetime

        monkeypatch.setattr(mod, "_DAILY_DIR_OVERRIDE", tmp_path)
        path = domain.daily_note_path(tmp_path)
        today = datetime.now().strftime("%Y-%m-%d")
        assert path.name == f"{today}.md"

    # -- _ensure_daily_note -----------------------------------------------

    def test_ensure_creates_file_when_missing(monkeypatch, tmp_path):
        monkeypatch.setattr(mod, "_DAILY_DIR_OVERRIDE", tmp_path)
        path = domain.ensure_daily_note(tmp_path)
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert content.startswith("# ")
        assert content.endswith("\n\n")

    def test_ensure_does_not_overwrite_existing(monkeypatch, tmp_path):
        monkeypatch.setattr(mod, "_DAILY_DIR_OVERRIDE", tmp_path)
        # Create the file first with custom content
        path = domain.daily_note_path(tmp_path)
        path.write_text("# existing content\n\nHello\n", encoding="utf-8")
        domain.ensure_daily_note(tmp_path)
        assert path.read_text(encoding="utf-8") == "# existing content\n\nHello\n"

    def test_ensure_creates_daily_dir_if_missing(monkeypatch, tmp_path):
        nested = tmp_path / "deep" / "daily"
        monkeypatch.setattr(mod, "_DAILY_DIR_OVERRIDE", nested)
        path = domain.ensure_daily_note(nested)
        assert nested.is_dir()
        assert path.exists()

    def test_daily_note_start_appends_timestamp_and_launches_cursor(
        monkeypatch, tmp_path
    ):
        monkeypatch.setattr(mod, "_DAILY_DIR_OVERRIDE", tmp_path)

        open_calls = []
        audio_calls = []
        ding_calls = []
        whisper_calls = []
        key_calls = []
        insert_calls = []
        sleep_calls = []

        actions.register_test_action(
            "user",
            "open_cursor_workspace",
            lambda path, fallback_to_terminal=False: open_calls.append(
                (path, fallback_to_terminal)
            ),
        )
        actions.register_test_action(
            "user",
            "audio_set_system_output_shokz",
            lambda: audio_calls.append("Shokz Loop110"),
        )
        actions.register_test_action("user", "play_ding", lambda: ding_calls.append(1))
        actions.register_test_action(
            "user", "whisper_normal", lambda: whisper_calls.append(1)
        )
        actions.register_test_action("", "key", lambda value: key_calls.append(value))
        actions.register_test_action(
            "", "insert", lambda value: insert_calls.append(value)
        )
        actions.register_test_action("", "sleep", lambda value: sleep_calls.append(value))

        actions.user.daily_note_start()

        note_path = domain.daily_note_path(tmp_path)
        content = note_path.read_text(encoding="utf-8")
        expected_line = str(content.count("\n") + 1)

        assert note_path.exists()
        assert content.startswith("# ")
        assert "\n## " in content
        assert open_calls == [(str(note_path), False)]
        assert audio_calls == ["Shokz Loop110"]
        assert len(ding_calls) == 1
        assert len(whisper_calls) == 1
        assert key_calls == ["ctrl-g", "enter", "end"]
        assert insert_calls == [expected_line]
        assert sleep_calls == ["2500ms", "300ms", "200ms", "100ms"]

    def test_save_shortcut_uses_cmd_on_mac():
        assert mod._save_shortcut("mac") == "cmd-s"

    def test_save_shortcut_uses_ctrl_on_windows():
        assert mod._save_shortcut("windows") == "ctrl-s"

    # -- daily_note_check logic -------------------------------------------

    def test_check_no_file_notifies_missing(monkeypatch, tmp_path):
        """When no daily note exists, check should notify and play cancel sound."""
        monkeypatch.setattr(mod, "_DAILY_DIR_OVERRIDE", tmp_path)
        cancel_calls = []
        actions.register_test_action("user", "play_cancel", lambda: cancel_calls.append(1))

        actions.user.daily_note_check()

        assert len(cancel_calls) == 1
        assert any("No daily note found" in n[1] for n in app.notifications)

    def test_check_recent_with_content_is_ok(monkeypatch, tmp_path):
        """Recently modified file with content after timestamp should be OK."""
        monkeypatch.setattr(mod, "_DAILY_DIR_OVERRIDE", tmp_path)
        path = domain.ensure_daily_note(tmp_path)

        # Write content with a timestamp and text after it
        path.write_text(
            "# 2026-03-23\n\n## 3:45 PM\n\nSome dictated notes here.\n",
            encoding="utf-8",
        )
        # Touch to make it recent
        os.utime(path, None)

        ding_calls = []
        actions.register_test_action("user", "play_ding", lambda: ding_calls.append(1))
        actions.register_test_action("user", "play_cancel", lambda: None)

        actions.user.daily_note_check()

        assert len(ding_calls) == 1
        assert any("Daily Note: OK" in n[0] for n in app.notifications)

    def test_check_uses_ctrl_s_on_windows(monkeypatch, tmp_path, talon_platform):
        monkeypatch.setattr(mod, "_DAILY_DIR_OVERRIDE", tmp_path)
        talon_platform("windows")
        path = domain.ensure_daily_note(tmp_path)
        path.write_text(
            "# 2026-03-23\n\n## 3:45 PM\n\nSome dictated notes here.\n",
            encoding="utf-8",
        )
        os.utime(path, None)

        key_calls = []
        actions.register_test_action("", "key", lambda value: key_calls.append(value))
        actions.register_test_action("user", "play_ding", lambda: None)
        actions.register_test_action("user", "play_cancel", lambda: None)

        actions.user.daily_note_check()

        assert key_calls == ["ctrl-s"]

    def test_check_recent_without_content_warns(monkeypatch, tmp_path):
        """Recently modified file with NO content after timestamp should warn."""
        monkeypatch.setattr(mod, "_DAILY_DIR_OVERRIDE", tmp_path)
        path = domain.ensure_daily_note(tmp_path)

        path.write_text("# 2026-03-23\n\n## 3:45 PM\n\n", encoding="utf-8")
        os.utime(path, None)

        cancel_calls = []
        actions.register_test_action("user", "play_ding", lambda: None)
        actions.register_test_action("user", "play_cancel", lambda: cancel_calls.append(1))

        actions.user.daily_note_check()

        assert len(cancel_calls) == 1
        assert any("No new content" in n[1] for n in app.notifications)

    def test_check_old_file_warns(monkeypatch, tmp_path):
        """File modified long ago should warn even if it has content."""
        monkeypatch.setattr(mod, "_DAILY_DIR_OVERRIDE", tmp_path)
        path = domain.ensure_daily_note(tmp_path)

        path.write_text(
            "# 2026-03-23\n\n## 3:45 PM\n\nSome content.\n",
            encoding="utf-8",
        )
        # Set modification time to 10 minutes ago
        old_time = time.time() - 600
        os.utime(path, (old_time, old_time))

        cancel_calls = []
        actions.register_test_action("user", "play_ding", lambda: None)
        actions.register_test_action("user", "play_cancel", lambda: cancel_calls.append(1))

        actions.user.daily_note_check()

        assert len(cancel_calls) == 1
        assert any("Daily Note: Check" in n[0] for n in app.notifications)

    def test_check_finds_last_timestamp_among_multiple(monkeypatch, tmp_path):
        """With multiple timestamps, check should look for content after the LAST one."""
        monkeypatch.setattr(mod, "_DAILY_DIR_OVERRIDE", tmp_path)
        path = domain.ensure_daily_note(tmp_path)

        path.write_text(
            "# 2026-03-23\n\n## 10:00 AM\n\nMorning notes.\n\n## 2:30 PM\n\n",
            encoding="utf-8",
        )
        os.utime(path, None)

        cancel_calls = []
        actions.register_test_action("user", "play_ding", lambda: None)
        actions.register_test_action("user", "play_cancel", lambda: cancel_calls.append(1))

        actions.user.daily_note_check()

        # Last timestamp (2:30 PM) has no content after it, so should warn
        assert len(cancel_calls) == 1
