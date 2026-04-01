"""Tests for shared platform helpers."""

import sys

if "pytest" in sys.modules:
    import user.talon_rebecca.core.platform_utils as platform_utils

    def test_command_with_directory_quotes_posix_paths_with_spaces():
        command = platform_utils.command_with_directory(
            "claude --dangerously-skip-permissions",
            "/tmp/project folder",
            os_name="posix",
        )

        assert command == "cd '/tmp/project folder'\nclaude --dangerously-skip-permissions"

    def test_command_with_directory_formats_windows_drive_changes():
        original_expand_path = platform_utils.expand_path
        platform_utils.expand_path = lambda path: r"C:\Users\rebec\project folder"
        try:
            command = platform_utils.command_with_directory(
                "codex --search",
                r"C:\Users\rebec\project folder",
                os_name="nt",
            )
        finally:
            platform_utils.expand_path = original_expand_path

        assert command == 'C:\ncd "C:\\Users\\rebec\\project folder"\ncodex --search'

    def test_quote_applescript_escapes_quotes_and_backslashes():
        quoted = platform_utils.quote_applescript(r'Hello "Cursor" \ docs')
        assert quoted == 'Hello \\"Cursor\\" \\\\ docs'
