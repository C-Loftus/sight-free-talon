import subprocess

from talon import Context, actions, settings

ctxMac = Context()
ctxMac.matches = r"""
os: mac
"""


@ctxMac.action_class("user")
class UserActions:
    def tts(text: str, interrupt: bool = True):
        """Text to speech with a robotic/narrator voice"""

        if interrupt:
            actions.user.cancel_current_speaker()

        speed = settings.get("user.tts_speed")
        # TODO: our speed is from -10 to 10 for espeak but needs
        # to be converted into words per min for say.

        proc = subprocess.Popen(["say", text])
        actions.user.set_cancel_callback(proc.kill)
