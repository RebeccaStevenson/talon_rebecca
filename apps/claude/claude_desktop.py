import subprocess

from talon import Module, app
from user.talon_rebecca.core.platform_utils import quote_applescript


mod = Module()

APP_NAME = "Claude"
def _menu_item_reference(path: list[str]) -> str:
    if len(path) < 2:
        raise ValueError("Menu path must include a top-level menu and an item")

    menu_name = quote_applescript(path[0])
    base = f'menu "{menu_name}" of menu bar item "{menu_name}" of menu bar 1'

    for submenu in path[1:-1]:
        submenu_name = quote_applescript(submenu)
        base = f'menu "{submenu_name}" of menu item "{submenu_name}" of {base}'

    final_name = quote_applescript(path[-1])
    return f'menu item "{final_name}" of {base}'


def _run_menu_path(menu_path: str) -> None:
    parts = [part.strip() for part in menu_path.split("|") if part.strip()]
    reference = _menu_item_reference(parts)
    script = f"""
tell application "{APP_NAME}" to activate
delay 0.15
tell application "System Events"
    tell process "{APP_NAME}"
        click {reference}
    end tell
end tell
"""
    subprocess.run(["osascript", "-e", script], check=True)


@mod.action_class
class Actions:
    def claude_desktop_menu(menu_path: str):
        """Select a Claude desktop macOS menu path like Help|Claude Help."""
        try:
            _run_menu_path(menu_path)
        except Exception as error:
            app.notify("Claude menu navigation failed", str(error))
