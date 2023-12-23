from talon import cron, Module, actions, app, settings

"""
Every 20 minutes, remind the user to take a break
to rest their eyes by looking at something 20 feet away
for 20 seconds.
"""

# Used for 20 / 20 / 20 rule
twenty_min = cron.seconds_to_timespec(20 * 60)

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
        notify("20 Elapsed")

cron.interval(twenty_min, break_wrapper)