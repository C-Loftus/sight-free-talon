from talon import Context, settings, actions
import os

from .sapi import SAPI5

if os.name == 'nt':
    speaker = SAPI5()


ctxWindows = Context()
ctxWindows.matches = r"""
os: windows
"""

@ctxWindows.action_class('user')
class UserActions:
    def base_win_tts(text: str, interrupt: bool):
        """Base function for windows tts. We expose this 
        so we can share the speaker object across files. We don't want 
        it to get overridden by the other tts functions"""
        speaker.set_rate(settings.get("user.tts_speed", 0))
        speaker.set_volume(settings.get("user.tts_volume", 50))
        speaker.speak(text, interrupt)

    def tts(text: str, interrupt:bool =True):
        """text to speech with windows voice"""
        # Base interrupt to the base
        actions.user.base_win_tts(text, interrupt)

    def toggle_reader():
        """Toggles the screen reader on and off"""
        actions.user.toggle_nvda()