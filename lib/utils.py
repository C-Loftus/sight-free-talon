import base64, enum
from talon import Module, actions, ui, Context, ctrl, clip, registry
import os, requests

mod = Module()

if os.name == 'nt':
    import winsound
 
class SpeakerType(enum.Enum):
    LIBRARY_CONTROLLER = 1
    SCHEDULED = 2
    NON_BLOCKING = 3

    
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

    def echo_tags():
        """Echo the current tags"""
        active_contexts = registry.tags
        actions.user.robot_tts(" ".join(active_contexts))


    def extract_text():
        """Extract the text from the current window"""

    def describe_image():
        """Describe the image on the clipboard"""

        image = clip.image().write_file("temp.png")

        # OpenAI API Key
        api_key = os.environ["OPENAI_API_KEY"]

        # Function to encode the image
        def encode_image(image_path):

            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')

        # Getting the base64 string
        base64_image = encode_image("temp.png")

        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
        }

        payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "What’s in this image?"
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
                }
            ]
            }
        ],
        "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        print(response.json())

    
ctxWindows = Context()
ctxWindows.matches = r"""
os: windows
"""

@ctxWindows.action_class("user")
class ActionsWin:
    def extract_text():
        """Extract the text from the current window. You 
        need powertoys or Windows 11 for this to work"""

        saved_x, saved_y = (actions.mouse_x(), actions.mouse_y())

        active_win = ui.active_window().rect
        actions.mouse_move(active_win.x, active_win.y)
        actions.user.notify(str(active_win.x) + " " + str(active_win.y) + " " + str(active_win.width) + " " + str(active_win.height))
        actions.key('super-shift-t')
        actions.sleep("2s")
        actions.mouse_drag(0)
        actions.sleep("1s")
        actions.mouse_move(active_win.x + active_win.width, active_win.y + active_win.height)
        actions.mouse_release(0)        
        actions.sleep("3s")
        actions.mouse_move(saved_x, saved_y)
    
    def beep(freq: int = 440, duration: int = 1000):
        """Beep"""
        winsound.Beep(freq, duration)


        