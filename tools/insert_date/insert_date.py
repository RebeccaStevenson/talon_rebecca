# Filename: insert_date.py
from talon import Module, actions
from datetime import datetime

mod = Module()

@mod.action_class
class Actions:
    def insert_current_date(format: str = "%Y-%m-%d"):
        """Inserts the current date at the cursor in the specified format."""
        date_str = datetime.now().strftime(format)
        actions.insert(date_str)
