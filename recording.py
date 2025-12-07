from talon import Module, actions

mod = Module()

@mod.action_class
class Actions:
    def recording_start():
        """Plays sound, waits, starts recording, and disables speech"""
        
        actions.user.play_ding()
        actions.sleep("1s")
        actions.user.system_command_nb("/bin/bash /Users/rebec/scripts/start_recording.sh")
        # actions.speech.disable()
        
    def recording_stop():
        """Stops recording and plays sound"""
        
        actions.user.system_command("/bin/bash /Users/rebec/scripts/stop_recording.sh")
        actions.user.play_thunk() 