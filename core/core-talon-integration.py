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

mod.setting(
    "tts_speed",
    type=float,
    default=1.0,
    desc="Speed of text to speech",
)

mod.setting(
    "echo_context",
    type=bool,
    default=False,
    desc="If true, plays back dictation with text to speech",
)

mod.setting(
    "tts_via_screenreader",
    type=bool,
    default=False,
    desc="If true, plays back dictation with text to speech through the screenreader, not within Talon",
)

mod.setting(
    "braille_output",
    type=bool,
    default=False,
    desc="If true, outputs braille through your screenreader",
)

ScreenreaderType = Literal["NVDA", "JAWS", "Narrator"]
mod.setting(
    "screenreader_type",
    type=ScreenreaderType,
    default="NVDA",
    desc="The screenreader you are using",
)


@mod.action_class
class Actions:
    def braille(text: str):
        """Output braille with the screenreader"""

    def cancel_robot_tts(text: str):
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


    def echo_context(include_title: bool = False):
        """Echo the current context"""
        friendly_name = actions.app.name() 
        title = ui.active_window().title 
        output = f"{friendly_name} {title}" if include_title else friendly_name
        actions.user.robot_tts(output)


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

def on_app_switch(app):
    if not settings.get("user.echo_context"):
        return 
    actions.user.echo_context()

# We have to keep track of the last title so we don't repeat it
# since sometimes Talon triggers a "title switch" when 
# the title actually hasn't changed, i.e. when a text file is saved
last_title = None
def on_title_switch(win):
    if not settings.get("user.echo_context"):
        return
    window = ui.active_window()
    active_window_title = window.title
    # get just the first two word
    active_window_title = ' '.join(active_window_title.split()[:2])
    #trime the title to 20 characters so super long addresses don't get read
    active_window_title = active_window_title[:20]

    global last_title
    if last_title == active_window_title:
        return
    else:
        last_title = active_window_title

    actions.user.robot_tts(f"{active_window_title}")

last_mode = None
def on_update_contexts():
    global last_mode
    modes = scope.get("mode") or []
    if last_mode == 'sleep' and 'sleep' not in modes:
        actions.user.robot_tts(f'Talon has waken up')
    last_mode = "sleep" if "sleep" in modes else "other"
        

registry.register("update_contexts", on_update_contexts)
ui.register("app_activate", on_app_switch)
ui.register("win_title", on_title_switch)
