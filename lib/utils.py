import base64, enum
from talon import Module, actions, ui, Context, ctrl, clip, registry
import os, requests
from .HTMLbuilder import HTMLBuilder

mod = Module()

if os.name == 'nt':
    import winsound

    
def remove_special(text):
    specialChars = ["'", '"', "(", ")", "[", "]", "{", "}", 
                    "<", ">", "|", "\\", "/", "_", "-", "+",
                    "=", "*", "&", "^", "%", "$", "#", "@", 
                    "!", "`", "~", "?", ",", ".", ":", ";"]
    
    for char in specialChars:
        text = text.replace(char, "")
    
    return text

@mod.action_class
class Actions:
    def indentation_level(text: str) -> int:
        '''count how many tabs are at the start of the line'''

        space_count = 0
        tab_count = 0
        for char in text:
            if char == '\t':
                tab_count += 1
            elif char == ' ':
                space_count += 1
            else:
                break  # Stop counting when a non-tab character is encountered
        # every 4 spaces is a tab
        tab_count += (space_count // 4)
        return tab_count

    def echo_context(include_title: bool = False):
        """Echo the current context"""
        friendly_name = actions.app.name() 
        title = ui.active_window().title 
        output = f"{friendly_name} {title}" if include_title else friendly_name
        actions.user.robot_tts(output)

    # def echo_tags():
    #     """Echo the current tags"""
    #     active_contexts = registry.tags
    #     actions.user.robot_tts(" ".join(active_contexts))

    def explore_tags():
        """Open the tags in the browser"""
        active_contexts = registry.tags
        builder = HTMLBuilder()
        builder.title("Talon Tags")
        for context in active_contexts:
            builder.p(context)
        builder.render()

    def explore_settings():
        """Open the talon settings file"""
        active_settings = registry.settings
        builder = HTMLBuilder()
        builder.title("Talon Settings")
        for setting in active_settings:
            builder.p(f"{setting}, {active_settings[setting]}")
        builder.render()

    def explore_modes():
        """Open the talon modes file"""

    def extract_text():
        """Extract the text from the current window"""

    
ctxWindows = Context()
ctxWindows.matches = r"""
os: windows
"""

@ctxWindows.action_class("user")
class ActionsWin:
    
    def beep(freq: int = 440, duration: int = 1000):
        """Beep"""
        winsound.Beep(freq, duration)
