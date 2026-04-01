from talon import Module, actions, app

mod = Module()


@mod.action_class
class Actions:
    def repeat_trailing_number(times: int = 1) -> None:
        """Repeat the current partial phrase for a trailing spoken number."""
        try:
            actions.core.repeat_partial_phrase(times)
        except IndexError:
            app.notify("Repeat", "No phrase to repeat.")
