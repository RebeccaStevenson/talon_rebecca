from talon import Context, Module

mod = Module()
ctx = Context()
ctx.matches = r"""
app: cursor
"""

# Define the list of available cursor models
mod.list("cursor_model", desc="Available Cursor AI models")
ctx.lists["user.cursor_model"] = {
    "o three": "o3-pro",
    "gemini": "gemini",
    "sonnet": "sonnet",
    "opus": "opus",
    "gpt": "gpt-4.1",
    "gpt four": "gpt-4.1",
    "max": "max",
    "auto": "auto",
}