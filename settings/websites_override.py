"""
Custom websites and search engines lists.

This module overrides the community website and search engine lists
with custom versions stored in talon_rebecca/settings/ so they won't
be overwritten when pulling community updates.
"""

import csv
from pathlib import Path

from talon import Context, resource

# Path to custom settings
SETTINGS_DIR = Path(__file__).parent

# More specific context to override the community defaults
ctx = Context()
ctx.matches = r"""
os: mac
"""


def parse_csv_to_dict(content: str, skip_header: bool = True) -> dict[str, str]:
    """Parse CSV content string into a dictionary."""
    rows = list(csv.reader(content.strip().split("\n")))
    mapping = {}

    start_row = 1 if skip_header and len(rows) > 0 else 0
    for row in rows[start_row:]:
        if len(row) == 0:
            continue
        if len(row) == 1:
            output = spoken_form = row[0]
        else:
            output, spoken_form = row[:2]
        spoken_form = spoken_form.strip()
        mapping[spoken_form] = output

    return mapping


# Watch websites.csv and update the list when it changes
websites_path = SETTINGS_DIR / "websites.csv"


@resource.watch(str(websites_path))
def on_websites_update(f):
    ctx.lists["user.website"] = parse_csv_to_dict(f.read())


# Watch search_engines.csv and update the list when it changes
search_engines_path = SETTINGS_DIR / "search_engines.csv"


@resource.watch(str(search_engines_path))
def on_search_engines_update(f):
    ctx.lists["user.search_engine"] = parse_csv_to_dict(f.read())

