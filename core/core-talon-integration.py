from typing import Optional
from talon import Module, actions, Context, settings, cron, ui, registry, scope, clip
import os,  subprocess
from ..lib import scheduling


if os.name == 'nt':
    import win32com.client

mod = Module()
ctx = Context()


@mod.action_class
class Actions:
    def braille(text: str):
        """Output braille with the screenreader"""

    def cancel_robot_tts():
        """Stop the currently spoken tts phrase"""

    def windows_native_tts(text: str):
        """text to speech with windows voice
         this function should never be overwritten and is used to be called from within the robot
         function which can be overwritten by the user
        """
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.rate = settings.get("user.tts_speed", 1.0)
        
        # send it to a central scheduler thread so it can be cancelled and so
        # it doesn't block the main thread or clog the log with warnings
        scheduling.Scheduler.send(speaker.Speak, text)

    def toggle_echo():
        """Toggles echo dictation on and off"""

        ctx.settings["user.echo_dictation"] = not settings.get("user.echo_dictation")
        if settings.get("user.echo_dictation"):
            actions.user.robot_tts("echo dictation enabled")
        else:
            actions.user.robot_tts("echo dictation disabled")
    
    def toggle_echo_context():
        """Toggles echo context on and off"""

        ctx.settings["user.echo_context"] = not settings.get("user.echo_context")
        if settings.get("user.echo_context"):
            actions.user.robot_tts("echo context enabled")
        else:
            actions.user.robot_tts("echo context disabled")
        

    def toggle_echo_all():
        """Toggles echo dictation and echo context on and off"""

        dictation, context = settings.get("user.echo_dictation"), settings.get("user.echo_context")

        if any([dictation, context]):
            actions.user.robot_tts("echo disabled")
            ctx.settings["user.echo_dictation"] = False
            ctx.settings["user.echo_context"] = False
        else:
            actions.user.robot_tts("echo enabled")
            ctx.settings["user.echo_dictation"] = True
            ctx.settings["user.echo_context"] = True


    def robot_tts(text: str):
        '''text to speech with robot voice'''


ctxWindows = Context()
ctxWindows.matches = r"""
os: windows
"""

@ctxWindows.action_class('user')
class UserActions:
    def robot_tts(text: str):
        """Text to speech with a robotic/narrator voice"""
        actions.user.windows_native_tts(text)


ctxLinux = Context()
ctxLinux.matches = r"""
os: linux
"""

@ctxLinux.action_class('user')
class UserActions:
    def robot_tts(text: str):
        """Text to speech with a robotic/narrator voice"""
        subprocess.Popen(["spd-say", text])
