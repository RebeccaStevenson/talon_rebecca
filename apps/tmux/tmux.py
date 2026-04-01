from talon import Module, actions

mod = Module()

@mod.action_class
class Actions:
    def tmux_prefix():
        """Send the tmux prefix (Ctrl-b)."""
        actions.key("ctrl-b")
        actions.sleep("50ms")

    def tmux_send(key_sequence: str, via_command: bool = False):
        """Send a tmux key sequence or command."""
        if via_command:
            actions.user.tmux_prefix()
            actions.key(":")
            actions.sleep("30ms")
            actions.insert(key_sequence)
            actions.key("enter")
        else:
            actions.user.tmux_prefix()
            actions.key(key_sequence)

    def tmux_keybind(direction: str):
        """Move to a tmux split in the given direction."""
        direction_map = {
            "left": "h",
            "down": "j",
            "up": "k",
            "right": "l",
        }
        key = direction_map.get(direction)
        if key:
            actions.user.tmux_send(key)
        else:
            actions.app.notify(f"Unknown direction: {direction}")

    def tmux_execute_command(command: str):
        """Execute a tmux command through the command prompt."""
        actions.user.tmux_send(command, via_command=True)
