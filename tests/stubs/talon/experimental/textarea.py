"""Stubs for talon.experimental.textarea."""


class Span:
    def __init__(self, left=0, right=0):
        self.left = left
        self.right = right


class DarkThemeLabels:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class LightThemeLabels:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TextArea:
    def __init__(self):
        self.title = ""
        self.value = ""
        self.theme = None
        self.sel = Span()
        self.rect = None
        self.showing = False

    def show(self):
        self.showing = True

    def hide(self):
        self.showing = False

    def register(self, event, callback):
        pass
