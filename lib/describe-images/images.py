from talon import Module, clip, Context, actions, ui
import requests, os, base64

mod = Module()

@mod.action_class
class Actions:
    def describe_image():
        """Describe the image on the clipboard"""

        clip.image().write_file("temp.png")

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

    def extract_text():
        """Extract text from the current focused window"""

        
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
        actions.key('super-shift-t')
        actions.sleep("2s")
        actions.mouse_drag(0)
        actions.sleep("1s")
        actions.mouse_move(active_win.x + active_win.width, active_win.y + active_win.height)
        actions.mouse_release(0)        
        actions.sleep("3s")
        actions.mouse_move(saved_x, saved_y)