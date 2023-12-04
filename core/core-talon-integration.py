from typing import Optional
from talon import Module, actions, Context, settings, cron, ui, registry, scope, clip, app  
import os,  subprocess
from ..lib import scheduling


if os.name == 'nt':
    import win32com.client

mod = Module()
ctx = Context()

# We want to get the settings from the talon file but then update 
    # them locally here so we can change them globally via expose talon actions

def initialize_settings():
    ctx.settings["user.echo_dictation"]: bool = settings.get("user.echo_dictation")
    ctx.settings["user.echo_context"]: bool = settings.get("user.echo_context")

# initialize the settings only after the user settings have been loaded
app.register('ready', initialize_settings)

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

    def echo_dictation_enabled() -> bool:
        """Returns true if echo dictation is enabled"""
        return ctx.settings["user.echo_dictation"]
    
    def echo_context_enabled() -> bool:
        """Returns true if echo context is enabled"""
        return ctx.settings["user.echo_context"]

    def toggle_echo():
        """Toggles echo dictation on and off"""

        if actions.user.echo_dictation_enabled():
            actions.user.robot_tts("echo disabled")
            ctx.settings["user.echo_dictation"] = False
        else:
            actions.user.robot_tts("echo enabled")
            ctx.settings["user.echo_dictation"] = True

    def toggle_echo_context():
        """Toggles echo context on and off"""

        if actions.user.echo_context_enabled():
            actions.user.robot_tts("echo context disabled")
            ctx.settings["user.echo_context"] = False
        else:
            actions.user.robot_tts("echo context enabled")
            ctx.settings["user.echo_context"] = True

    def toggle_echo_all():
        """Toggles echo dictation and echo context on and off"""

        dictation, context = actions.user.echo_dictation_enabled(), actions.user.echo_context_enabled()

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

    def espeak(text: str):
        '''text to speech with espeak'''


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

def remove_special(text):
    specialChars = ["'", '"', "(", ")", "[", "]", "{", "}", 
                    "<", ">", "|", "\\", "/", "_", "-", "+",
                    "=", "*", "&", "^", "%", "$", "#", "@", 
                    "!", "`", "~", "?", ",", ".", ":", ";"]
    
    for char in specialChars:
        text = text.replace(char, "")
    
    return text


@ctxLinux.action_class('user')
class UserActions:
    def espeak(text: str):
        """Text to speech with a robotic/narrator voice"""
        rate = settings.get("user.tts_speed", 0)
        # convert -5 to 5 to -100 to 100 
        rate = rate * 20
        text = remove_special(text)

        subprocess.Popen(["spd-say", text, "--rate", str(rate)])


    def robot_tts(text: str):
        """Text to speech with a robotic/narrator voice"""
        # change the directory to the directory of this file
        # so we can run the command from the correct directory
        model_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "additional_voices", "models")
        piper = os.path.expanduser("~/.local/bin/piper")

        os.chdir(model_dir)

        modes = ['en_US-amy-low.onnx', 'en_US-lessac-medium.onnx']

        high = 22050
        low = 16000

        #  we need this more verbose representation here so we don't use this 
        # shell and have risks of shell expansion
        command1 = ["echo", f"{text}"]

        command2 = [piper, "--model", modes[0], "--length_scale", "0.5", "--output_raw"]

        command3 = ["aplay", "-r", str(low), "-c", "1", "-f", "S16_LE", "-t", "raw"]

        process1 = subprocess.Popen(command1, stdout=subprocess.PIPE)
        process2 = subprocess.Popen(command2, stdin=process1.stdout, stdout=subprocess.PIPE)
        process1.stdout.close()
        process3 = subprocess.Popen(command3, stdin=process2.stdout)
        process2.stdout.close()




ctxMac = Context()
ctxMac.matches = r"""
os: mac
"""

@ctxMac.action_class('user')
class UserActions:
    def robot_tts(text: str):
        """Text to speech with a robotic/narrator voice"""
        os.system(f"say '{text}'")

    
