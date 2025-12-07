from talon import Module, actions

mod = Module()

@mod.action_class
class Actions:
    # Primary controls
    def whisper_start():
        """Starts Superwhisper and disables Talon speech"""
        actions.speech.disable()
        actions.key("alt-cmd-r")

    def whisper_stop(wake_talon: bool = True):
        """Stops Superwhisper and optionally enables Talon speech"""
        actions.key("alt-cmd-r")
        if wake_talon:
            actions.speech.enable()

    def whisper_cancel():
        """Cancels Superwhisper and enables Talon speech"""
        actions.speech.enable()
        actions.key("esc")

    def whisper_toggle_mode():
        """Toggles Superwhisper mode"""
        actions.key("alt-cmd-u")

    # Mode switching
    def whisper_local():
        """Disables speech and switches Superwhisper to local mode"""
        actions.speech.disable()
        actions.user.superwhisper_local_mode()

    def whisper_normal():
        """Enables speech and switches Superwhisper to normal mode"""
        actions.speech.enable()
        actions.user.superwhisper_normal_mode()

    # Helper functions (called by mode switching)
    def superwhisper_local_mode():
        """Switches Superwhisper to local mode"""
        actions.user.system_command_nb("/bin/bash /Users/rebec/scripts/superwhisper_local_mode.sh")

    def superwhisper_normal_mode():
        """Switches Superwhisper to normal mode"""
        actions.user.system_command_nb("/bin/bash /Users/rebec/scripts/superwhisper_normal_mode.sh")
