from talon import Module, actions, ui, Context, ctrl, clip, registry, scope
import os, requests
from html.parser import HTMLParser
import urllib

from ..lib.HTMLbuilder import HTMLBuilder
import threading

class VisibleTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.ignore = False
        self.ignore_tags = ['style', 'script', 'head', 'title', 'meta', '[document]']

    def handle_starttag(self, tag, attrs):
        if tag in self.ignore_tags:
            self.ignore = True

    def handle_endtag(self, tag):
        if tag in self.ignore_tags:
            self.ignore = False

    def handle_data(self, data):
        if not self.ignore:
            self.text.append(data.strip())


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
        actions.user.tts(output)

    # def echo_tags():
    #     """Echo the current tags"""
    #     active_contexts = registry.tags
    #     actions.user.tts(" ".join(active_contexts))

    def explore_tags():
        """Open the tags in the browser"""
        active_contexts = registry.tags
        builder = HTMLBuilder()
        builder.title("Talon Tags")
        builder.h1("Currently Active Tags")
        for context in active_contexts:
            builder.p(context)
        builder.render()

    def explore_settings():
        """Open the talon settings file"""
        active_settings = registry.settings
        builder = HTMLBuilder()
        builder.title("Talon Settings")
        builder.h1("Talon Settings and their Values")
        for setting in active_settings:
            builder.p(f"{setting}, {active_settings[setting]}")
        builder.render()

    def explore_modes():
        """Open the talon modes file"""

    def extract_text():
        """Extract the text from the current window"""

    def echo_mode():
        """Echo the current modes"""
        modes = scope.get("mode")
        # if dictation or command is in the modes, say that first
        if "dictation" in modes and "command" in modes:
            actions.user.tts("mixed")
        elif "dictation" in modes:
            actions.user.tts("dictation")
        elif "command" in modes:
            actions.user.tts("command")

    def get_website_text(url: str) -> str:
        """Get the visible text from a website"""
        try:
            # Download HTML content
            with urllib.request.urlopen(url) as response:
                html_content = response.read()

            # Parse HTML and extract visible text
            parser = VisibleTextParser()
            parser.feed(html_content.decode('utf-8', errors='ignore'))

            # Combine and return the visible text
            return ' '.join(parser.text)

        except Exception as e:
            print("Error Parsing:", e)
            return f"Error Parsing"



    
ctxWindows = Context()
ctxWindows.matches = r"""
os: windows
"""

@ctxWindows.action_class("user")
class ActionsWin:
    
    def beep(freq: int = 440, duration: int = 1000):
        """Beep"""
        t = threading.Thread(target=winsound.Beep, args=(freq, duration))
        t.start()
