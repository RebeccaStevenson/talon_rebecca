"""Windows-specific app discovery and launch helpers."""

from __future__ import annotations

import os
import subprocess
from itertools import chain
from pathlib import Path

from talon import ui

from user.talon_rebecca.core.app_switcher.matching import (
    duplicates_removed,
    hierarchical_name_match,
)


def list_appx_packages() -> list[dict[str, str]]:
    """Return Windows AppX package metadata from PowerShell."""
    out = subprocess.check_output(
        'powershell.exe -WindowStyle hidden -ExecutionPolicy Bypass -Command "Get-AppxPackage"',
        shell=False,
        text=True,
    )
    apps: list[dict[str, str]] = []
    for app_text in out.split("\n\n"):
        app_dict: dict[str, str] = {}
        lines = app_text.split("\n")
        if len(lines) <= 1:
            continue
        for line in lines:
            sections = line.split(":")
            if len(sections) >= 2:
                app_dict[sections[0].strip()] = ":".join(sections[1:])[1:]
        apps.append(app_dict)
    return apps


def _start_menu_shortcuts() -> list[tuple[str, Path]]:
    lnk_pattern = "**/*.lnk"
    system_start_programs_path = (
        Path(os.environ.get("PROGRAMDATA", "")) / "Microsoft/Windows/Start Menu/Programs"
    )
    user_start_programs_path = (
        Path(os.environ.get("APPDATA", "")) / "Microsoft/Windows/Start Menu/Programs"
    )
    desktop_path = Path(os.environ.get("APPDATA", "")) / "Desktop"

    programs = [
        (path.stem.lower(), path)
        for path in chain(
            desktop_path.glob(lnk_pattern),
            user_start_programs_path.glob(lnk_pattern),
            system_start_programs_path.glob(lnk_pattern),
        )
    ]
    programs = duplicates_removed(programs)
    programs.sort(key=lambda item: len(item[0]))
    return programs


def launch_program_windows(
    program_name: str,
    *,
    match_start: bool = True,
    match_fuzzy: bool = True,
) -> None:
    """Launch a Windows program by exact path, AppX package, or shortcut."""
    try:
        ui.launch(path=program_name)
        return
    except FileNotFoundError:
        pass

    appx_targets = [
        (app["Name"], app["PackageFamilyName"])
        for app in list_appx_packages()
        if "Name" in app and "PackageFamilyName" in app
    ]
    matching_apps = hierarchical_name_match(
        program_name,
        appx_targets,
        match_start,
        match_fuzzy,
        match_fuzzy,
    )
    if matching_apps:
        subprocess.run(
            ["explorer.exe", f"shell:AppsFolder\\{matching_apps[0]}!App"],
            shell=False,
            check=False,
        )
        return

    matching_paths = hierarchical_name_match(
        program_name.lower(),
        _start_menu_shortcuts(),
        match_start,
        match_fuzzy,
        match_fuzzy,
    )
    if matching_paths:
        os.startfile(str(matching_paths[0]))
        return

    raise ValueError(f'Program could not be started: "{program_name}"')
