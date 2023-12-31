from talon import Context, actions
import subprocess

ctxMac = Context()
ctxMac.matches = r"""
os: mac
"""

@ctxMac.action_class('user')
class UserActions:
    def tts(text: str):
        """Text to speech with a robotic/narrator voice"""
        # We can't really schedule this since it is a system command, so we
        # have to spawn a new process each time unfortunately
        proc = subprocess.Popen(["say", text])
        actions.user.set_cancel_callback(proc.kill)

    
