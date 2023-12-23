from talon import actions, Module, settings, cron, Context, clip, registry, app 
import os, ctypes, time , sys

mod = Module()
ctx = Context()

mod.tag("orca_running", desc="If set, orca is running")

@mod.scope
def set_orca_running_tag():
    '''Update tags based on if Orca is running'''
    # TODO edge case on startup this might not be set yet
    try:
        ctx.tags = ["user.orca_running"] \
            if actions.user.is_orca_running() \
            else []
    except:
        ctx.tags = []

if sys.platform == "linux" or sys.platform.startswith("linux"):
    cron.interval("3s", set_orca_running_tag.update)



@mod.action_class
class Actions:
    def is_orca_running() -> bool:
        '''Returns true if orca is running'''
        return True if "user.orca_running" in ctx.tags else False
    
    def orca_tts(text: str, use_clipboard: bool= False):
        '''text to speech with orca'''


ctxLinux = Context()
ctx.matches = r"""
os: linux
"""

@ctxLinux.action_class("user")
class LinuxActions:
    def toggle_reader():
        '''Toggles orca on and off'''
        if not os.path.exists("/usr/bin/orca"):
            actions.user.tts("Orca is not installed")
            return

        actions.key("alt-super-s")

ctxorcaRunning = Context()
ctxorcaRunning.matches = r"""
tag: user.orca_running
"""


@ctxorcaRunning.action_class("user")
class orcaActions:
    def orca_tts(text: str, use_clipboard: bool= False):
        """text to speech with orca"""
