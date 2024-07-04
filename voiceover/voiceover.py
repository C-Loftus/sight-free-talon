import os
import sys

from talon import Context, Module, actions, cron, settings, ui

mod = Module()
ctx = Context()
ctx.matches = r"""
os: mac
"""

from talon.mac import applescript

@ctx.action_class("user")
class MacActions:
    def toggle_reader():
        actions.key("cmd-f5")

    def with_voiceover_mod_press(key: str):
        """Presses the given key with the voiceover modifier key"""
        voiceover_key = settings.get("user.voiceover_key")
        actions.key(f"{voiceover_key}:down")
        actions.sleep("100ms")
        actions.key(key)
        actions.sleep("10ms")
        actions.key(f"{voiceover_key}:up")


mod.tag("voiceover_running", desc="If set, voiceover is running")

@mod.scope
def set_voiceover_running_tag():
    """Update tags based on if voiceover is running"""
    # Edge case on startup this might not be set yet we we catch all exceptions

    try:
        ctx.tags = (
            ["user.voiceover_running"] if actions.user.is_voiceover_running() else []
        )
    except Exception:
        ctx.tags = []


if sys.platform == "darwin":
    cron.interval("3s", set_voiceover_running_tag.update)


@mod.action_class
class Actions:
    def is_voiceover_running() -> bool:
        """Returns true if voiceover is running"""
        if os.name != "darwin":
            return False
        
        # TODO : figure out how a way to check this without spamming subprocesses
        return False

    def voiceover_tts(text: str):
        """text to speech with voiceover"""

    def with_voiceover_mod_press(key: str):
        """Presses the given key with the voiceover modifier key"""
        voiceover_key = settings.get("user.voiceover_key")
        actions.key(f"{voiceover_key}:down")
        actions.sleep("50ms")
        actions.key(key)
        actions.sleep("10ms")
        actions.key(f"{voiceover_key}:up")


ctxVoiceoverRunning = Context()
ctxVoiceoverRunning.matches = r"""
tag: user.voiceover_running
"""


@ctxVoiceoverRunning.action_class("user")
class VoiceoverActions:
    def tts(text: str, interrupt: bool = True):
        """text to speech with voiceover"""
        

        def wrapper(text):
            res = applescript.run(
            f"""

            tell application "VoiceOver"
                output "{text}"
            end tell
            """
            )
        # spawn it on a different thread so if it stalls we don't hang
        cron.after("0s", lambda: wrapper(text))

