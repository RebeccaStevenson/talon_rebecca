"""
Actions that manage personal notes, including daily logs and therapy updates.
"""
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

from talon import Module, actions, app

mod = Module()
_IS_MAC = app.platform == "mac"
NOTES_DIR = Path("/Users/rebec/Library/CloudStorage/Dropbox/DropboxDocuments/notes")


def _open_path(path: Path) -> None:
    if _IS_MAC:
        subprocess.run(["open", str(path)], check=False)
    else:
        os.startfile(path, "open")  # type: ignore[attr-defined]


@mod.action_class
class Actions:
    def maybe_disable_speech_for_notes(path: str) -> None:
        """Conditionally run commands if the file is notes.md."""
        filename = os.path.basename(path)

        if filename == "journal.md" or filename == "physical_therapy_daily.md":
            actions.user.insert_current_date("%A, %B %d, %Y")
            actions.sleep("200ms")
            actions.key("enter:3")
            actions.sleep("200ms")
            actions.key("up:2")
            actions.sleep("100ms")

            actions.speech.disable()
            actions.key("alt-cmd-r")
        else:
            actions.key("enter:2")
            actions.key("up:2")

    def create_note() -> None:
        """Create a new timestamped note."""
        NOTES_DIR.mkdir(parents=True, exist_ok=True)
        curtime = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        file_path = NOTES_DIR / f"{curtime}.md"
        file_path.touch()
        actions.sleep("500ms")
        _open_path(file_path)

    def append_to_daily_note_text(text: str) -> None:
        """Append provided text to the daily note."""
        NOTES_DIR.mkdir(parents=True, exist_ok=True)
        file_path = NOTES_DIR / "daily note.md"
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(text + "\n")

    def create_or_append_date_note_text(text: Optional[str] = None) -> None:
        """Create or append provided text to the date-named note."""
        NOTES_DIR.mkdir(parents=True, exist_ok=True)
        curdate = datetime.now().strftime("%Y-%m-%d")
        file_path = NOTES_DIR / f"{curdate}.md"
        if text:
            with open(file_path, "a", encoding="utf-8") as file:
                file.write(text + "\n")
        else:
            if not file_path.exists():
                file_path.touch()

    def add_note_to_physical_therapy(text: str) -> None:
        """Add a new note to the top of the physical therapy document."""
        file_path = Path(
            r"C:\Users\rebec\Dropbox\DropboxDocuments\notes\physical_therapy_daily.md"
        )
        current_date = datetime.now().strftime("%A, %B %d, %Y")

        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as file:
                existing_content = file.read()
        else:
            existing_content = ""

        new_content = f"{current_date}\n{text}\n\n{existing_content}"

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(new_content)

        print(f"Added new note to {file_path}")
