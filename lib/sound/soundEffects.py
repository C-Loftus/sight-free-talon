import os
import subprocess
import threading
import time

from talon import Context, Module

if os.name == "nt":
    import winsound

mod = Module()


@mod.action_class
class Actions:
    def play_loading_sound():
        """Play a sound to indicate that the command is being processed"""

    def play_error_sound():
        """Play a sound to indicate that the command has failed"""

    def play_success_sound():
        """Play a sound to indicate that the command has succeeded"""


def stop_loading_sound():
    """Stop the loading sound"""
    global cancel_signal
    cancel_signal = True


linux_context = Context()
linux_context.matches = r"""
os: linux
"""

windows_context = Context()
windows_context.matches = r"""
os: windows
"""

mac_context = Context()
mac_context.matches = r"""
os: mac
"""

cancel_signal = False

sound_path = os.path.join(os.path.dirname(__file__), "assets")
loading_sound = os.path.join(sound_path, "loading.wav")
error_sound = os.path.join(sound_path, "error.wav")
success_sound = os.path.join(sound_path, "success.wav")


@linux_context.action_class("user")
class LinuxActions:
    def play_loading_sound():
        """Play a sound to indicate that the command is being processed"""
        # use aplay to continuously play a sound signifying loading

        def play_sound():
            global cancel_signal
            while True and not cancel_signal:
                subprocess.run(["aplay", loading_sound])
                time.sleep(1)

            # reset the cancel signal if it was used to stop the sound
            cancel_signal = False

        # start a new thread to play the sound
        t = threading.Thread(target=play_sound)
        t.start()

    def play_error_sound():
        """Play a sound to indicate that the command has failed"""
        # use aplay to play a sound signifying an error
        stop_loading_sound()
        subprocess.Popen(["aplay", error_sound])

    def play_success_sound():
        """Play a sound to indicate that the command has succeeded"""
        # use aplay to play a sound signifying success
        stop_loading_sound()
        subprocess.Popen(["aplay", success_sound])


@mac_context.action_class("user")
class MacActions:
    def play_loading_sound():
        """Play a sound to indicate that the command is being processed"""
        # use aplay to continuously play a sound signifying loading

        def play_sound():
            global cancel_signal
            while True and not cancel_signal:
                subprocess.run(["afplay", loading_sound])
                time.sleep(1)

            # reset the cancel signal if it was used to stop the sound
            cancel_signal = False

        # start a new thread to play the sound
        t = threading.Thread(target=play_sound)
        t.start()

    def play_error_sound():
        """Play a sound to indicate that the command has failed"""
        # use aplay to play a sound signifying an error
        stop_loading_sound()
        subprocess.Popen(["afplay", error_sound])

    def play_success_sound():
        """Play a sound to indicate that the command has succeeded"""
        # use aplay to play a sound signifying success
        stop_loading_sound()
        subprocess.Popen(["afplay", success_sound])


@windows_context.action_class("user")
class WindowsActions:
    def play_loading_sound():
        """Play a sound to indicate that the command is being processed"""
        # use aplay to continuously play a sound signifying loading

        def play_sound():
            global cancel_signal
            while True and not cancel_signal:
                winsound.PlaySound(
                    loading_sound, winsound.SND_FILENAME | winsound.SND_ASYNC
                )
                time.sleep(1)

            # reset the cancel signal if it was used to stop the sound
            cancel_signal = False

        # start a new thread to play the sound
        t = threading.Thread(target=play_sound)
        t.start()

    def play_error_sound():
        """Play a sound to indicate that the command has failed"""
        # use winsound to play a sound signifying an error
        stop_loading_sound()
        winsound.PlaySound(error_sound, winsound.SND_FILENAME | winsound.SND_ASYNC)

    def play_success_sound():
        """Play a sound to indicate that the command has succeeded"""
        # use winsound to play a sound signifying success
        stop_loading_sound()
        winsound.PlaySound(success_sound, winsound.SND_FILENAME | winsound.SND_ASYNC)
