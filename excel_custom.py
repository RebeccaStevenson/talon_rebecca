from talon import ui, Module, Context, registry, actions, imgui, cron, app
import os
from typing import Optional
from datetime import datetime, timedelta, date

mod = Module()
ctx = Context()

mod = Module()
is_mac = app.platform == "mac"


@mod.action_class
class Actions:
    def get_column_number(column_name: str):
        """Return the 1-based column index for the requested header."""
        column_headers = [
            "Unnamed: 0",
            "WristEx",
            "HandEx",
            "LegEx",
            "AnkleEx",
            "TopStretch",
            "LowerStretch",
            "TopMove",
            "LowerMove",
            "Psoas",
            "Walk",
            "Cardio",
            "One",
            "WakeTime",
            "Tired",
            "Work",
            "Tea",
            "Stress",
            "Mood",
            "Pain",
            "Notes",
            "Notes2",
            "Notes3",
        ]

        if column_name in column_headers:
            return column_headers.index(column_name) + 1
        return None

    def find_current_date_row_number():
        """Calculate the current date row index."""
        start_date = datetime(2024, 3, 1)
        current_date = datetime.now()
        delta_days = (current_date - start_date).days
        # account for header rows
        return 3 + delta_days

    def press_ctrl_home():
        """Cross-platform ctrl+home."""
        if is_mac:
            actions.key("cmd-home")
        else:
            actions.key("ctrl-home")

    def press_ctrl_g():
        """Cross-platform ctrl+g."""
        if is_mac:
            actions.key("ctrl-g")
            actions.sleep("25ms")
            actions.key("tab")
        else:
            actions.key("ctrl-g")

    def go_to_cell(column: str):
        """Navigate to the cell in the requested column for the current date row."""
        column_number = actions.user.get_column_number(column)
        row_number = actions.user.find_current_date_row_number()
        if column_number is None or row_number is None:
            actions.app.notify("Unable to resolve column or row for go_to_cell")
            return

        actions.user.press_ctrl_home()
        actions.key("{down:" + str(row_number - 2))
        actions.key("right:" + str(column_number - 1))
        actions.insert("")

    def go_column(column: str):
        """Jump to the specified column header."""
        column_number = actions.user.get_column_number(column)
        if column_number is None:
            actions.app.notify(f"Unknown column: {column}")
            return
        actions.key("home")
        actions.key("right:" + str(column_number - 1))

    def go_today():
        """Jump to the current day's row in column B."""
        row_number = actions.user.find_current_date_row_number()
        if row_number is None:
            actions.app.notify("Unable to determine current date row")
            return
        actions.user.press_ctrl_g()
        actions.sleep("50ms")
        actions.insert(f"B{row_number}")
        actions.key("enter")
