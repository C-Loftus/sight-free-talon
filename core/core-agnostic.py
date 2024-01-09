"""
This file contains actions that are core to the talon tts system
and are agnostic to the tts voice being used or the operating system
"""

from typing import Optional
from talon import Module, actions, Context, settings, app

mod = Module()
ctx = Context()

# We want to get the settings from the talon file but then update 
    # them locally here so we can change them globally via expose talon actions
def initialize_settings():
    ctx.settings["user.echo_dictation"]: bool = settings.get("user.echo_dictation", True)
    ctx.settings["user.echo_context"]: bool = settings.get("user.echo_context", False)

# initialize the settings only after the user settings have been loaded
app.register('ready', initialize_settings)


speaker_cancel_callback: Optional[callable] = None

@mod.action_class
class Actions:
    def set_cancel_callback(callback: callable):
        """
        Sets the callback to call when the current speaker is cancelled. Only 
        necessary to set if the tts is coming from a subprocess where we need to store a handle
        """
        global speaker_cancel_callback 
        speaker_cancel_callback = callback

    def cancel_current_speaker():
        """Cancels the current speaker"""
        global speaker_cancel_callback
        if not speaker_cancel_callback:
            return
        
        try:
            speaker_cancel_callback()
        except Exception as e:
            print(e)
        finally:
            speaker_cancel_callback = None
            


    def braille(text: str):
        """Output braille with the screenreader"""

    def echo_dictation_enabled() -> bool:
        """Returns true if echo dictation is enabled"""
        return ctx.settings["user.echo_dictation"]
    
    def echo_context_enabled() -> bool:
        """Returns true if echo context is enabled"""
        return ctx.settings["user.echo_context"]

    def toggle_echo():
        """Toggles echo dictation on and off"""

        if actions.user.echo_dictation_enabled():
            actions.user.tts("echo disabled")
            ctx.settings["user.echo_dictation"] = False
        else:
            actions.user.tts("echo enabled")
            ctx.settings["user.echo_dictation"] = True

    def toggle_echo_context():
        """Toggles echo context on and off"""

        if actions.user.echo_context_enabled():
            actions.user.tts("echo context disabled")
            ctx.settings["user.echo_context"] = False
        else:
            actions.user.tts("echo context enabled")
            ctx.settings["user.echo_context"] = True

    def toggle_echo_all():
        """Toggles echo dictation and echo context on and off"""

        dictation, context = actions.user.echo_dictation_enabled(), actions.user.echo_context_enabled()

        if any([dictation, context]):
            actions.user.tts("echo disabled")
            ctx.settings["user.echo_dictation"] = False
            ctx.settings["user.echo_context"] = False
        else:
            actions.user.tts("echo enabled")
            ctx.settings["user.echo_dictation"] = True
            ctx.settings["user.echo_context"] = True


    def tts(text: str):
        '''text to speech with robot voice'''
        print("Sight-Free-Talon Error: TTS not implemented in this context")

    def espeak(text: str):
        '''text to speech with espeak'''
        actions.user.tts("Espeak Not Supported In This Context")

    def toggle_reader():
        """Toggles the screen reader on and off"""
        actions.user.tts("Toggle Reader Not Supported In This Context")

    def base_win_tts(text: str):
        """Base function for windows tts. We expose this 
        so we can share the speaker object across files since 
        it won't get overridden by the other tts functions"""

    def switch_voice():
        """Switches the tts voice"""
        actions.user.tts("Switching Not Supported In This Context")

    
    def piper(text: str):
        """Text to speech with a piper model"""