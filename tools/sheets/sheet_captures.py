from dataclasses import dataclass

from talon import Module, actions

mod = Module()

@dataclass
class Cell:
    column: str
    row: int

@dataclass
class CellRange:
    start: Cell
    end: Cell

@mod.capture(rule="<user.letters> <user.number_string>")
def cell(m) -> Cell:
    """A spreadsheet cell."""
    return Cell(column=m.letters, row=m.number_string)

@mod.capture(rule="<user.cell> past <user.cell>")
def cell_range(m) -> CellRange:
    """A spreadsheet cell range."""
    return CellRange(start=m.cell_1, end=m.cell_2)