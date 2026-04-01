"""Declarative app-launch specs used by system.programs wrappers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProgramSpec:
    start_name: str
    focus_name: str | None = None
    focus_title: str | None = None
    start_delay: str = "2000ms"
    launch_only: bool = False


PROGRAM_SPECS: dict[str, ProgramSpec] = {
    "firefox": ProgramSpec(start_name="firefox", start_delay="5000ms"),
    "chrome": ProgramSpec(start_name="chrome"),
    "discord": ProgramSpec(start_name="discord"),
    "slack": ProgramSpec(start_name="slack", launch_only=True),
    "rider": ProgramSpec(start_name="rider"),
    "blender": ProgramSpec(start_name="blender"),
    "unreal_engine": ProgramSpec(
        start_name="Unreal Engine",
        focus_name="UnrealEditor",
    ),
    "task_manager": ProgramSpec(start_name="task manager"),
    "command_prompt": ProgramSpec(start_name="command prompt"),
    "powershell": ProgramSpec(start_name="powershell"),
    "windows_terminal": ProgramSpec(start_name="terminal"),
    "windows_explorer": ProgramSpec(
        start_name="file explorer",
        focus_name="windows explorer",
    ),
    "epic_games": ProgramSpec(
        start_name="epic games",
        focus_name="EpicGames",
    ),
    "whatsapp": ProgramSpec(
        start_name="WhatsApp",
        focus_name="Application Frame Host",
        focus_title="WhatsApp",
    ),
}
