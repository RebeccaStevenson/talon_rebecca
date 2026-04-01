from pathlib import Path

from talon import Context

_REPO_ROOT = Path(__file__).resolve().parents[2]
_VOCAB_FILE = _REPO_ROOT / "settings" / "vocabulary.talon-list"

ctx = Context()
ctx.matches = "os: mac"


@ctx.action_class("user")
class UserActions:
    def get_vocabulary_file_path():
        """Return the canonical Rebecca vocabulary file."""
        return str(_VOCAB_FILE)
