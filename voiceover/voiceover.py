from talon import Context, Module, actions

mod = Module()
ctx = Context()
ctx.matches = r"""
os: mac
"""


@ctx.action_class("user")
class UserActions:
    def toggle_reader():
        actions.key("cmd-f5")
