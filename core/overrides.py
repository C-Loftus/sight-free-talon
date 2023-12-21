from talon import actions, Context, settings, Module, app

ctx = Context()

disable_keypresses = False
sound_on_keypress = False

# Set psuedo tags for the user's settings that can be switched on and off
def set_tags():
    global disable_keypresses, sound_on_keypress
    disable_keypresses = True if settings.get("user.disable_keypresses", False) else False
    sound_on_keypress = True if settings.get("user.sound_on_keypress", False) else False

app.register("ready", set_tags)

@ctx.action_class("main")
class MainOverrides():
    def key(key: str):
        global disable_keypresses, sound_on_keypress

        if settings.get("user.disable_keypresses", False) or disable_keypresses:
            print("A key was pressed but sight-free-talon has disabled keypresses")
            return
        
        elif settings.get("user.sound_on_keypress", False) or sound_on_keypress:
            actions.user.beep()

        actions.next(key)


mod = Module()

@mod.action_class
class ActionsToCall():
    def toggle_keypress_sound():
        """Toggles whether or not to play a sound on keypress"""
        global sound_on_keypress
        sound_on_keypress = not sound_on_keypress

    def toggle_keypresses():
        """Toggles whether or not to pass keypresses through to the OS"""
        global sound_on_keypress
        sound_on_keypress = not sound_on_keypress