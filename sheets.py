from talon import Module, clip, actions
import re

from .sheet_captures import Cell, CellRange

mod = Module()

mod.apps.google_sheets = r"""
tag: browser
browser.host: docs.google.com
browser.path: /^/spreadsheets/.*/
"""
mod.apps.google_sheets = r"""
app.name: Sheets
"""

# Matches single cell and cell ranges.
CELL_REGEX = r"([A-Za-z]+)(\d+)(?::([A-Za-z]+)(\d+))?"

def get_current_location() -> Cell | CellRange:
    actions.edit.copy()
    actions.sleep("100ms")
    location = clip.text()
    match = re.match(CELL_REGEX, location)
    if match.group(3) is None: # [column, row, None, None]
        return Cell(column=match.group(1), row=match.group(2))
    if match.group(3) is not None: # [column, row, column, row]
        return CellRange(start=Cell(column=match.group(1), row=match.group(2)),
                         end=Cell(column=match.group(3), row=match.group(4)))
    raise Exception("Unknown cell format:", location)

@mod.action_class
class Actions:
    def select_row(row: str):
        """Maintaining the current column position(s), select the given row."""
        actions.user.chrome_mod("j")
        loc = get_current_location()
        if isinstance(loc, Cell):
            actions.insert(f"{loc.column}{row}")
        elif isinstance(loc, CellRange):
            actions.insert(f"{loc.start.column}{row}:{loc.end.column}{row}")
        actions.key("enter")

    def select_column(col: str):
        """Maintaining the current row position(s), select the given column."""
        actions.user.chrome_mod("j")
        loc = get_current_location()
        if isinstance(loc, Cell):
            actions.insert(f"{col}{loc.row}")
        elif isinstance(loc, CellRange):
            actions.insert(f"{col}{loc.start.row}:{col}{loc.end.row}")
        actions.key("enter")

    def select_cell(cell: Cell):
        """Selects the cell, without placing the cursor inside."""
        actions.user.chrome_mod("j")
        actions.key("backspace")
        actions.sleep("50ms")
        actions.user.insert_formatted(cell.column, "ALL_CAPS")
        actions.insert(cell.row)
        actions.key("enter")

    def select_cell_range(cell_range: CellRange):
        """Selects the cell range, without placing the cursor inside."""
        actions.user.chrome_mod("j")
        actions.key("backspace")
        actions.sleep("50ms")
        actions.user.insert_formatted(cell_range.start.column, "ALL_CAPS")
        actions.insert(cell_range.start.row)
        actions.insert(":")
        actions.user.insert_formatted(cell_range.end.column, "ALL_CAPS")
        actions.insert(cell_range.end.row)
        actions.key("enter")

    def reselect_cell_range(cell: Cell):
        """
        Corrects a selection by reselecting the end marker.
        Can also be used to extend a single cell to a range by setting the end marker.
        """
        actions.user.chrome_mod("j")
        loc = get_current_location()
        if isinstance(loc, Cell):
            actions.insert(f"{loc.column}{loc.row}:{cell.column}{cell.row}")
        if isinstance(loc, CellRange):
            actions.insert(f"{loc.start.column}{loc.start.row}:{cell.column}{cell.row}")
        actions.key("enter")
