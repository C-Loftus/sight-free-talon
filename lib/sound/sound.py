import os

from talon import Context, Module

if os.name == "nt":
    import winsound

mod = Module()


@mod.action_class
class Actions:
    def beep(freq: int = 440, duration: int = 1000):
        """Beep a sound"""


ctxWindows = Context()
ctxWindows.matches = r"""
os: windows
"""


@ctxWindows.action_class("user")
class ActionsWin:
    def beep(freq: int = 440, duration: int = 1000):
        """Beep"""
        winsound.Beep(freq, duration)
