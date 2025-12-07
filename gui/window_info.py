from talon import ui, Module, Context, registry, actions, imgui, cron
import time

try:
    from win32gui import GetWindowText, GetForegroundWindow
except ImportError:  # macOS / Linux
    GetWindowText = None
    GetForegroundWindow = None

mod = Module()

@imgui.open(x=0, y=30)
def window_info(gui: imgui.GUI):
    gui.text(f"{ui.active_app()}")
    gui.text(f"{ui.active_app().exe}")
    gui.text(f"{ui.active_window().title}")
    if GetForegroundWindow and GetWindowText:
        hwnd = GetForegroundWindow()
        gui.text(f"{hwnd}")
        gui.text(f"{GetWindowText(hwnd)}")
        try:
            gui.text(f"{GetWindowText(ui.active_window().id)}")
        except TypeError:
            gui.text("Win32 window id unavailable")
    else:
        gui.text("Win32 window APIs unavailable on this platform")
    gui.text(f"")

    for c in reversed(registry.active_contexts()):
        if not c.path.startswith("user."): continue
        if not c.path.endswith(".talon"): continue
        p = c.path[5:-6]
        gui.text(f"- {p}")

    time.sleep(0.1)

@mod.action_class
class Actions:
    def window_info_toggle():
        """toggle window info imgui"""
        window_info.hide() if window_info.showing else window_info.show()
