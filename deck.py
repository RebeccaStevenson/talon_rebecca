from talon import Module, actions, scope

mod = Module()

@mod.action_class
class Actions:
    def deck_toggle_talon_speech():
        """Toggles Talon speech on or off"""
        if "sleep" in scope.get("mode"):
            actions.speech.enable()
            actions.user.play_ding()
        else:
            actions.speech.disable()
            actions.user.play_thunk()
