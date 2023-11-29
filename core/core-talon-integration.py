from typing import Optional
from talon import Module, actions, Context, settings, cron, ui, registry, scope, clip
import requests
import json, os, time, subprocess, multiprocessing
from pathlib import Path
from typing import Literal


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
        # Moves the tts to the cron thread,
        # However, this blocks the cron thread until the tts is done
        # TODO: make this not block the cron thread 
        # by passing to a designated tts thread. (We
        # don't want to make a new thread each time
        # since that will through an error in the log
        # every time and spam the log, and thus tts)
        cron.after("0s", lambda: speaker.Speak(text))

        # TODO:  this doesn't work to stop text to speech in the middle of speaking
        # # for some reason, TODO fix this
        #  
        # global TTS_IN_PROGRESS
        # if TTS_IN_PROGRESS:
        #     if not TTS_IN_PROGRESS.stopped():
        #         actions.user.notify('stopped')
        #         TTS_IN_PROGRESS.stop()
            
        # TTS_IN_PROGRESS = StoppableThread(target=speaker.Speak, args=(text,))
        # TTS_IN_PROGRESS.start()

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