from talon import Module, actions
import subprocess

mod = Module()

@mod.action_class
class Actions:
    def switch_audio_output():
        """Switches audio output device using a menu"""
        command = ["/opt/homebrew/bin/SwitchAudioSource", "-a"]  # Use full path
        result = subprocess.run(command, capture_output=True, text=True)
        devices = result.stdout.splitlines()

        if not devices:
            actions.app.notify("No audio devices found!")
            return

        def set_device(device):
            subprocess.run(["/opt/homebrew/bin/SwitchAudioSource", "-s", device], check=True)
            actions.app.notify(f"Switched to: {device}")

        # Use Talon's built-in menu
        chosen_device = actions.app.choice("Choose Audio Output", devices)
        if chosen_device:
            set_device(chosen_device)
