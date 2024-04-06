# from __future__ import absolute_import
# import pywintypes

import os

from talon import Context, Module, actions, cron

# class Jaws():
#     """Supports the Jaws for Windows screen reader."""

#     name = "jaws"

#     def __init__(self, *args, **kwargs):
#         super(Jaws, self).__init__(*args, **kwargs)
#         try:
#             self.object = load_com("FreedomSci.JawsApi", "jfwapi")
#         except (pywintypes.com_error, TypeError):
#             raise OutputError

#     def braille(self, text, **options):
#         # HACK: replace " with ', Jaws doesn't seem to understand escaping them with \
#         text = text.replace('"', "'")
#         self.object.RunFunction('BrailleString("%s")' % text)

#     def speak(self, text, interrupt=False):
#         self.object.SayString("      %s" % text, interrupt)

#     def is_active(self):
#         try:
#             import win32gui
#         except ImportError:
#             return False
#         try:
#             return (
#                 self.object.SayString("", 0) == True
#                 or win32gui.FindWindow("JFWUI2", "JAWS") != 0
#             )
#         except:
#             return False


mod = Module()
ctx = Context()

mod.tag("jaws_running", desc="If set, JAWS is running")


@mod.scope
def set_jaws_running_tag():
    """Update tags based on if JAWS is running"""
    # TODO edge case on startup this might not be set yet
    try:
        ctx.tags = ["user.jaws_running"] if actions.user.is_jaws_running() else []
    except Exception:
        ctx.tags = []


if os.name == "nt":
    cron.interval("3s", set_jaws_running_tag.update)


@mod.action_class
class Actions:
    def toggle_jaws():
        """Toggles JAWS on and off"""

    def restart_jaws():
        """Restarts JAWS"""

    def is_jaws_running() -> bool:
        """Returns true if JAWS is running"""

    def jaws_tts(text: str, use_clipboard: bool = False):
        """text to speech with JAWS"""


ctxWindowsJAWSRunning = Context()
ctxWindowsJAWSRunning.matches = r"""
os: windows
tag: user.jaws_running
"""
