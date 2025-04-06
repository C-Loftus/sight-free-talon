import ctypes
import os
import time
import subprocess
from talon import Context, Module, actions, cron, speech_system, settings, scope, clip

mod = Module()
ctx = Context()

mod.tag("jaws_running", desc="If set, JAWS is running")


@mod.scope
def set_jaws_running_tag():
    """Update tags based on if JAWS is running"""
    try:
        ctx.tags = ["user.jaws_running"] if actions.user.is_jaws_running() else []
    except Exception:
        ctx.tags = []


if os.name == "nt":
    # Load the JAWS COM object for speech synthesis
    try:
        import win32com.client
        jaws = win32com.client.Dispatch("FreedomSci.JawsApi")
    except Exception as e:
        jaws = None

    cron.interval("3s", set_jaws_running_tag.update)


@mod.action_class
class Actions:
    def toggle_jaws():
        """Toggles JAWS on and off"""
        if not actions.user.is_jaws_running():
            actions.key("ctrl-alt-j")
            actions.user.tts("Turning JAWS on using shortcut control+alt+j")
        else:
            actions.user.tts("Turning JAWS off")
            time.sleep(1)
            actions.user.with_jaws_mod_press("j")
            time.sleep(0.5)
            actions.key("x")

    def restart_jaws():
        """Restarts JAWS"""
        if actions.user.is_jaws_running():
            actions.user.with_jaws_mod_press("control-f4")

    def with_jaws_mod_press(keys: str):
        """Presses the JAWS modifier key in combonation with provided keys. A cama sepparated list of keys can be provided for actions that require holding the jaws modifier while pressing keys more than once."""
        key_list = keys.split(",")
        jaws_key = settings.get("user.jaws_key")
        actions.key(f"{jaws_key}:down")
        try:
            for key in key_list:
                # actions.sleep("10ms")
                actions.key(key.strip())
            actions.sleep("10ms")
        finally:
            actions.key(f"{jaws_key}:up")

    def with_jaws_mod_layered_key_presses(keys: str):
        """Presses the JAWS modifier key in combonation with the first provided keys in the list. A cama sepparated list of keys to be pressed without the jaws modifier can be provided, for layered keyboard commands."""
        key_list = keys.split(",")
        jaws_keystroke = key_list.pop(0).strip()
        jaws_key = settings.get("user.jaws_key")
        actions.key(f"{jaws_key}:down")
        try:
            actions.sleep("50ms")
            actions.key(jaws_keystroke)
            actions.sleep("10ms")
            actions.key(f"{jaws_key}:up")

            for key in key_list:
                actions.sleep("100ms")
            actions.key(key.strip())
        finally:
            actions.key(f"{jaws_key}:up")

    def is_jaws_running() -> bool:
        """Returns true if JAWS is running"""
        if os.name != "nt" or jaws is None:
            return False

        try:
            # Test if JAWS is running by invoking a function from the API
            return jaws.SayString("", False)  # If JAWS is running, this should not throw an error
        except Exception:
            return False

    def jaws_tts(text: str, use_clipboard: bool = False):
        """text to speech with JAWS"""

    def test_jaws_api():
        """Test the JAWS API connection"""
        if jaws:
            jaws.SayString("Testing JAWS integration.", False)
        else:
            actions.user.tts("Failed to connect to JAWS API.")


ctxWindowsJAWSRunning = Context()
ctxWindowsJAWSRunning.matches = r"""
os: windows
tag: user.jaws_running
"""


@ctxWindowsJAWSRunning.action_class("user")
class UserActions:
    def jaws_tts(text: str, use_clipboard: bool = False):
        """text to speech with JAWS"""
        if not jaws:
            errorMessage = str(ctypes.WinError(1))
            raise Exception(f"Error communicating between Talon and JAWS: {errorMessage}", e)

        if use_clipboard:
            with clip.revert():
                clip.set_text(text)  # sets the result to the clipboard
                actions.sleep("50ms")
                actions.user.with_jaws_mod_press("super-x")
        else:
            jaws.SayString(text, False)

    def tts(text: str, interrupt: bool = True):
        """Text to speech within JAWS"""
        if settings.get("user.tts_via_screenreader"):
            cron.after("300ms", lambda: actions.user.jaws_tts(text))
        else:
            actions.user.base_win_tts(text, interrupt)

    def cancel_current_speaker():
        """Cancel JAWS speech"""
        if jaws:
            jaws.StopSpeech()

    def braille(text: str):
        """Output braille with JAWS"""
        if jaws:
            # HACK: replace " with ', Jaws doesn't seem to understand escaping them with \
            text = text.replace('"', "'")
            jaws.RunFunction(f'BrailleString("{text}")')

    def switch_voice():
        """Switches the voice for the screen reader"""
        actions.user.tts("You must switch voice in JAWS manually")


ctxWindowsJAWSRunning = Context()
ctxWindowsJAWSRunning.matches = r"""
os: windows
tag: user.jaws_running
"""
