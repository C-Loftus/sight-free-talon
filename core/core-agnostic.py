"""
This file contains actions that are core to the talon tts system
and are agnostic to the tts voice being used or the operating system
"""

from typing import Callable, ClassVar, Optional

from talon import Context, Module, actions, app, settings

mod = Module()
ctx = Context()


class AgnosticState:
    speaker_cancel_callback: ClassVar[Optional[Callable]] = None


# We want to get the settings from the talon file but then update
# them locally here so we can change them globally via exposed talon actions
def initialize_settings():
    ctx.settings["user.echo_dictation"] = settings.get("user.echo_dictation", True)
    ctx.settings["user.echo_context"] = settings.get("user.echo_context", False)
    ctx.settings["user.echo_braille"] = settings.get("user.echo_braille", True)


# initialize the settings only after the user settings have been loaded
app.register("ready", initialize_settings)

speaker_cancel_callback: Optional[Callable] = None


@mod.action_class
class Actions:
    def set_cancel_callback(callback: Callable):
        """
        Sets the callback to call when the current speaker is cancelled. Only
        necessary to set if the tts is coming from a subprocess where we need to store a handle
        """
        AgnosticState.speaker_cancel_callback = callback

    def cancel_current_speaker():
        """Cancels the current speaker"""
        if not AgnosticState.speaker_cancel_callback:
            return

        try:
            AgnosticState.speaker_cancel_callback()
        except Exception as e:
            print(e)
        finally:
            AgnosticState.speaker_cancel_callback = None

    def braille(text: str):
        """Output braille with the screenreader"""
        raise NotImplementedError

    def toggle_braille():
        """Toggles braille on and off"""
        if actions.user.braille_enabled():
            actions.user.tts("braille disabled")
            ctx.settings["user.echo_braille"] = False
        else:
            actions.user.tts("braille enabled")
            ctx.settings["user.echo_braille"] = True

    def echo_dictation_enabled() -> bool:
        """Returns true if echo dictation is enabled"""
        # Catch potential race condition where settings haven't been loaded at startup
        try:
            return ctx.settings["user.echo_dictation"]
        except Exception:
            return False

    def braille_enabled() -> bool:
        """Returns true if braille is enabled"""
        # Catch potential race condition where settings haven't been loaded at startup
        try:
            return ctx.settings["user.echo_braille"]
        except Exception:
            return False

    def echo_context_enabled() -> bool:
        """Returns true if echo context is enabled"""
        # Catch potential race condition where settings haven't been loaded at startup
        try:
            return ctx.settings["user.echo_context"]
        except Exception:
            return False

    def toggle_echo() -> None:
        """Toggles echo dictation on and off"""

        if actions.user.echo_dictation_enabled():
            actions.user.tts("echo disabled")
            ctx.settings["user.echo_dictation"] = False
        else:
            actions.user.tts("echo enabled")
            ctx.settings["user.echo_dictation"] = True

    def toggle_echo_context() -> None:
        """Toggles echo context on and off"""

        if actions.user.echo_context_enabled():
            actions.user.tts("echo context disabled")
            ctx.settings["user.echo_context"] = False
        else:
            actions.user.tts("echo context enabled")
            ctx.settings["user.echo_context"] = True

    def toggle_echo_all() -> None:
        """Toggles echo dictation and echo context on and off"""

        dictation, context = (
            actions.user.echo_dictation_enabled(),
            actions.user.echo_context_enabled(),
        )

        if any([dictation, context]):
            actions.user.tts("echo disabled")
            ctx.settings["user.echo_dictation"] = False
            ctx.settings["user.echo_context"] = False
        else:
            actions.user.tts("echo enabled")
            ctx.settings["user.echo_dictation"] = True
            ctx.settings["user.echo_context"] = True

    def tts(text: str, interrupt: bool = True):
        """text to speech with robot voice"""
        raise NotImplementedError(
            "Sight-Free-Talon Error: TTS not implemented in this context"
        )

    def espeak(text: str):
        """text to speech with espeak"""
        actions.user.tts("Espeak Not Supported In This Context")
        raise NotImplementedError

    def toggle_reader():
        """Toggles the screen reader on and off"""
        actions.user.tts("Toggle Reader Not Supported In This Context")
        raise NotImplementedError

    def base_win_tts(text: str, interrupt: bool):
        """Base function for windows tts. We expose this
        so we can share the speaker object across files since
        it won't get overridden by the other tts functions"""
        raise NotImplementedError

    def switch_voice():
        """Switches the tts voice"""
        actions.user.tts("Switching Not Supported In This Context")
        raise NotImplementedError

    def piper(text: str):
        """Text to speech with a piper model"""
        raise NotImplementedError
