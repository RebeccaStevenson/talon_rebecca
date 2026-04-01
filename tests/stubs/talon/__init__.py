"""Talon stubs for pytest.

Extended from community/test/stubs/talon/__init__.py with additional
stubs for APIs used by talon_rebecca scripts (ui.active_window,
app.notify, clip, scope).
"""

import inspect
from types import SimpleNamespace
from typing import Callable


class RegisteredActionsAccessor:
    def __init__(self, registered_actions, namespace):
        self.registered_actions = registered_actions
        self.namespace = namespace

    def __getattr__(self, name):
        for category in ("test", "module"):
            cat_actions = self.registered_actions[category]
            if self.namespace in cat_actions:
                if name in cat_actions[self.namespace]:
                    return cat_actions[self.namespace][name]

        raise AttributeError(f"Couldn't find action {self.namespace}.{name}")

    def __call__(self, *args, **kwargs):
        raise RuntimeError(f"actions.{self.namespace}() is not an available action")


class Actions:
    """Implements something like talon.actions."""

    def __init__(self):
        self.registered_actions = {
            "module": {},
            "test": {},
        }

        # Some built in actions
        self.register_module_action("", "key", lambda x: None)
        self.register_module_action("", "insert", lambda x: None)
        self.register_module_action("", "sleep", lambda x: None)
        self.register_module_action("edit", "selected_text", lambda: "test")

    def reset_test_actions(self):
        self.registered_actions["test"] = {}

    def register_module_action(self, namespace: str, name: str, func: Callable):
        self._register_action("module", namespace, name, func)

    def register_test_action(self, namespace: str, name: str, func: Callable):
        self._register_action("test", namespace, name, func)

    def _register_action(
        self, category: str, namespace: str, name: str, func: Callable
    ):
        if namespace not in self.registered_actions[category]:
            self.registered_actions[category][namespace] = {}
        self.registered_actions[category][namespace][name] = func

    def __getattr__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            pass

        try:
            default_accessor = RegisteredActionsAccessor(self.registered_actions, "")
            return getattr(default_accessor, name)
        except AttributeError:
            return RegisteredActionsAccessor(self.registered_actions, name)


class Module:
    """Implements something like the Module class built in to Talon."""

    def __init__(self):
        self.apps = SimpleNamespace()

    def list(self, *args, **kwargs):
        pass

    def setting(self, *args, **kwargs):
        pass

    def capture(self, rule=None):
        def __funcwrapper(func):
            def __inner(*args, **kwargs):
                return func(*args, **kwargs)

            return __inner

        return __funcwrapper

    def tag(self, name, desc=None):
        pass

    def action_class(self, target_class):
        for name, func in inspect.getmembers(target_class, inspect.isfunction):
            actions.register_module_action("user", name, func)
        return target_class


class Context:
    """Implements something like the Context class built in to Talon."""

    lists = {}
    tags = []

    def __init__(self, *args, **kwargs):
        pass

    def action_class(self, path=None):
        def __funcwrapper(clazz):
            return clazz

        return __funcwrapper

    def capture(self, name: str, rule: str = None):
        def __funcwrapper(func):
            def __inner(*args, **kwargs):
                return func(*args, **kwargs)

            return __inner

        return __funcwrapper


class _GuiHandle:
    """Stub for the object returned by @imgui.open()."""

    showing = False

    def show(self):
        self.showing = True

    def hide(self):
        self.showing = False


class ImgUI:
    """Stub out ImgUI so we don't get crashes."""

    GUI = None

    def open(self, **kwargs):
        def __funcwrapper(func):
            handle = _GuiHandle()
            handle._func = func
            return handle

        return __funcwrapper


# ---------------------------------------------------------------------------
# Window / UI stubs
# ---------------------------------------------------------------------------

class _Window:
    """Mutable window object returned by ui.active_window()."""

    def __init__(self):
        self.title = ""
        self.hidden = False
        self.app = SimpleNamespace(name="")

    def focus(self):
        pass


class _Screen:
    """Stub for a screen/display object."""

    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 1920
        self.height = 1080


class UI:
    """Stub for talon.ui with active_window() and main_screen() support."""

    class UIErr(Exception):
        pass

    def __init__(self):
        self._window = _Window()
        self._windows = []
        self._screen = _Screen()
        self._apps = []

    def active_window(self):
        return self._window

    def apps(self, background=False):
        return self._apps

    def launch(self, path=None):
        pass

    def windows(self):
        return self._windows

    def main_screen(self):
        return self._screen

    def register(self, *args, **kwargs):
        pass


# ---------------------------------------------------------------------------
# Clip stub
# ---------------------------------------------------------------------------

class _Clip:
    """Stub for talon.clip with text() / set_text()."""

    def __init__(self):
        self._text = ""

    def text(self):
        return self._text

    def get(self):
        return self._text

    def set_text(self, value: str):
        self._text = value


# ---------------------------------------------------------------------------
# App stub (with notify recording)
# ---------------------------------------------------------------------------

class App:
    """Stub for talon.app with platform and notify()."""

    platform = "mac"

    def __init__(self):
        self.notifications = []

    def notify(self, title: str = "", body: str = ""):
        self.notifications.append((title, body))


# ---------------------------------------------------------------------------
# Settings / Resource / Scope stubs
# ---------------------------------------------------------------------------

class Settings:
    """Implements something like talon.settings."""


class Resource:
    """Implements something like the talon resource system."""

    def open(self, path: str, mode: str = "r"):
        return open(path, mode, encoding="utf-8")


class Scope:
    """Stub for talon.scope."""

    def get(self, key, default=None):
        return default


class Cron:
    """Stub for talon.cron."""

    def interval(self, _spec, _func):
        return object()

    def after(self, _spec, _func):
        return object()

    def cancel(self, _job):
        pass


# ---------------------------------------------------------------------------
# Module-level singletons (importable as `from talon import actions, app, ...`)
# ---------------------------------------------------------------------------

actions = Actions()
app = App()
clip = _Clip()
imgui = ImgUI()
ui = UI()
settings = Settings()
resource = Resource()
scope = Scope()
cron = Cron()

# Indicate to test files that they should load since we're running in test mode
test_mode = True
