from talon import Context, settings
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
    def base_win_tts(text: str):
        """Base function for windows tts. We expose this 
        so we can share the speaker object across files. We don't want 
        it to get overridden by the other tts functions"""
        speaker.set_rate(settings.get("user.tts_speed", 0))
        speaker.set_volume(settings.get("user.tts_volume", 50))
        speaker.speak(text, interrupt=True)

    def tts(text: str):
        """text to speech with windows voice"""
        actions.user.base_win_tts(text)

    def toggle_reader():
        """Toggles the screen reader on and off"""
        actions.user.toggle_nvda()