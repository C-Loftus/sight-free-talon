from talon import actions, Module, settings, cron, Context, clip, registry
import os, ctypes

# Load the NVDA client library
dir_path = os.path.dirname(os.path.realpath(__file__))
dll_path = os.path.join(dir_path, "nvdaControllerClient64.dll")
nvda_client: ctypes.WinDLL = ctypes.windll.LoadLibrary(dll_path)

mod = Module()
ctx = Context()

mod.tag("nvda_running", desc="NVDA is running")

mod.setting(
    "nvda_key",
    type=str,
    default="capslock",
    desc="The key that is used as the NVDA key",
)


@mod.scope
def set_nvda_running_tag():
    '''Update tags based on if NVDA is running'''
    ctx.tags = ["user.nvda_running"] \
        if actions.user.is_nvda_running() \
        else []

# Re-run the above code to update the scope
cron.interval("3s", set_nvda_running_tag.update)


@mod.action_class
class Actions:
     
    def toggle_nvda():
        '''Toggles NVDA on and off'''
        if not actions.user.is_nvda_running():
            actions.key("ctrl-alt-n") 
            actions.user.robot_tts("Turning NVDA on")
        elif actions.user.is_nvda_running():
            actions.user.with_nvda_mod_press('q')
            actions.user.robot_tts("Turning NVDA off")


    def with_nvda_mod_press(key: str):
        """Presses the NVDA key"""
        nvda_key = settings.get("user.nvda_key")
        actions.key(f'{nvda_key}:down') 
        actions.sleep("50ms")
        actions.key(key)
        actions.sleep("10ms")
        actions.key(f'{nvda_key}:up') 

    def is_nvda_running() -> bool:
        '''Returns true if NVDA is running'''
        return True if nvda_client.nvdaController_testIfRunning() == 0 else False
    
    def nvda_tts(text: str, use_clipboard: bool= False):
        '''text to speech with NVDA'''

ctxNVDARunning = Context()
ctxNVDARunning.matches = r"""
tag: user.nvda_running
"""


@ctxNVDARunning.action_class("user")
class NVDAActions:
    def nvda_tts(text: str, use_clipboard: bool= False):
        """text to speech with NVDA"""

        # Test if NVDA is running, and if its not show a message
        res = nvda_client.nvdaController_testIfRunning()
        if res != 0:
            errorMessage = str(ctypes.WinError(res))
            # ctypes.windll.user32.MessageBoxW(0, "Error: %s" % errorMessage, "Error communicating between Talon and NVDA", 0)
            raise Exception("Error communicating between Talon and NVDA: %s" % errorMessage)

        # Text can be sent via the clipboard or directly to NVDA using the dll
        if use_clipboard:
            with clip.revert():
                clip.set_text(text) # sets the result to the clipboard
                actions.sleep("50ms")
                actions.user.with_nvda_mod_press('c')
        else:
            nvda_client.nvdaController_speakText(text)


ctxWindowsNVDARunning = Context()
ctxWindowsNVDARunning.matches = r"""
os: windows
tag: user.nvda_running
"""
@ctxWindowsNVDARunning.action_class('user')
class UserActions:
    
    def robot_tts(text: str):
        """Text to speech"""
        if settings.get("user.tts_via_screenreader"):
            actions.user.nvda_tts(text)
        else:
            actions.user.windows_native_tts(text)

    def cancel_robot_tts(text: str):
        """Cancel the narrator tts from NVDA"""
        nvda_client.nvdaController_cancelSpeech()

    def braille_output(text: str):
        """Output braille with NVDA"""
        nvda_client.nvdaController_brailleMessage(text)