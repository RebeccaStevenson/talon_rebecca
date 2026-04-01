"""Global fallback for opening-number commands."""

from talon import Module, app


module = Module()


@module.action_class
class ModuleActions:
    def opening_number_action(number: int) -> None:
        """Context-specific command that fires on an opening number."""
        # Override this with any DWIM number action that is useful in a specific
        # context.
        #
        # This is defined here so the DFA graph doesn't have to be recompiled
        # every time there is a context switch between states with/without
        # opening number actions.
        print(f"Got repeat {number} without prior command, ignoring.")
        app.notify(
            "Number DWIM", "No opening number actions available in this context."
        )
