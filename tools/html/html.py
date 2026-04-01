from talon import Context, Module, actions

mod = Module()
mod.tag("html", desc="tag for enabling html commands")

ctx = Context()
ctx.matches = r"""
app: vscode
app: cursor
"""
ctx.tags = ["user.html"]

@mod.action_class
class Actions:
    def insert_mark():
        """surrounds the selected text with a mark tag using the clipboard"""
        # 1. Get the selected text. This safely uses the clipboard.
        selected_text = actions.edit.selected_text()

        if selected_text:
            # 2. Add the wrapping.
            wrapped_text = f"<mark>{selected_text}</mark>"

            # 3. Replace the selection with the enhanced wrapped text via paste.
            actions.user.paste(wrapped_text) 