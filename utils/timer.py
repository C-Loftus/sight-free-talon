from talon import cron, Module, actions, app, settings, app
import os
if os.name == "nt":
    import ctypes

"""
Every certain amount of minutes, remind the user to take a break
to rest their eyes by looking at something 20 feet away
for at least 20 seconds.
"""


# Defaults to Andreas' notification system, but falls back to Talon's
def notify(message: str):
    try:
        actions.user.notify(message)
    except:
        app.notify(message)
    print(message)

mod = Module()


def break_wrapper():
    if settings.get("user.enable_break_timer"):
        actions.user.eye_break_callback()

@mod.action_class
class Actions:
    def eye_break_callback():
        """
        Reminds you to take a break once 
        the timer is triggered
        """
        # Intentionally vague in case you are in a meeting
        if os.name == "nt":
            # ctypes.windll.user32.MessageBoxW(0, "Elapsed", "Notification", 1)
            actions.user.tts("Elapsed")
            actions.user.with_nvda_mod_press('ctrl-escape')
        else:
            notify("Elapsed")


def set_timer():
    ten_min = cron.seconds_to_timespec(settings.get("user.min_until_break") * 60)
    cron.interval(ten_min, break_wrapper)

app.register("ready", set_timer)


