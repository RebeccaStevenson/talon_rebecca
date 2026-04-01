from talon import Module

mod = Module()


@mod.capture(rule="<user.ordinal_or_last>")
def cursorless_ordinal_or_last(m) -> int:
    return m.ordinal_or_last
