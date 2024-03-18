from talon import Context, actions, settings
import os
import subprocess
from typing import Literal

ctxLinux = Context()
ctxLinux.matches = r"""
os: linux
"""


speaker: Literal["espeak", "piper"] = "espeak"


@ctxLinux.action_class("user")
class UserActions:
    def toggle_reader():
        """Toggles the screen reader on and off"""
        actions.user.toggle_orca()

    def switch_voice():
        """Switches the tts voice"""
        global speaker
        if speaker == "espeak":
            speaker = "piper"
            actions.user.tts("Switched to piper")
        else:
            speaker = "espeak"
            actions.user.tts("Switched to espeak")

    def tts(text: str, interrupt: bool = True):
        """Text to speech with a robotic/narrator voice"""
        if interrupt:
            actions.user.cancel_current_speaker()

        match speaker:
            case "espeak":
                actions.user.espeak(text)
            case "piper":
                actions.user.piper(text)
            case _:
                raise ValueError(f"Unknown speaker {speaker}")

    def espeak(text: str):
        """Text to speech with a robotic/narrator voice"""
        rate = settings.get("user.tts_speed")
        # convert -10 to 10 to -100 to 100
        rate = rate * 10

        # text = remove_special(text)

        volume = settings.get("user.tts_volume")

        # volume is from 1 to 100, convert it to -100 to 100
        volume = int(volume - 50) * 2

        proc = subprocess.Popen(
            ["spd-say", text, "--rate", str(rate), "--volume", str(volume)]
        )
        actions.user.set_cancel_callback(proc.kill)

    def piper(text: str):
        """Text to speech with a robotic/narrator voice"""
        # change the directory to the directory of this file
        # so we can run the command from the correct directory
        model_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "additional_voices", "models"
        )
        # You have to install piper with pipx
        piper = os.path.expanduser("~/.local/bin/piper")

        os.chdir(model_dir)

        modes = ["en_US-amy-low.onnx", "en_US-lessac-medium.onnx"]
        # high = 22050
        # Hz for playback in low quality
        low = 16000

        #  we need this more verbose representation here so we don't use the
        # shell and have risks of shell expansion
        command1 = ["echo", f"{text}"]
        command2 = [piper, "--model", modes[0], "--length_scale", "0.5", "--output_raw"]
        command3 = ["aplay", "-r", str(low), "-c", "1", "-f", "S16_LE", "-t", "raw"]

        echo = subprocess.Popen(command1, stdout=subprocess.PIPE)
        piper = subprocess.Popen(command2, stdin=echo.stdout, stdout=subprocess.PIPE)
        echo.stdout.close()
        aplay = subprocess.Popen(command3, stdin=piper.stdout)
        piper.stdout.close()
        actions.user.set_cancel_callback(aplay.kill)
