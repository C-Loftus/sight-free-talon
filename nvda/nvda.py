from talon import actions, Module, settings, cron, Context, clip, registry, app , speech_system
import os, ctypes, time  

mod = Module()
ctx = Context()

mod.tag("nvda_running", desc="If set, NVDA is running")

@mod.scope
def set_nvda_running_tag():
    '''Update tags based on if NVDA is running'''
    # TODO edge case on startup this might not be set yet
    try:
        ctx.tags = ["user.nvda_running"] \
            if actions.user.is_nvda_running() \
            else []
    except:
        ctx.tags = []

if os.name == 'nt':
    # Load the NVDA client library
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dll_path = os.path.join(dir_path, "nvdaControllerClient64.dll")
    nvda_client: ctypes.WinDLL = ctypes.windll.LoadLibrary(dll_path)

    cron.interval("3s", set_nvda_running_tag.update)
else:
    nvda_client = None


@mod.action_class
class Actions:
     
    def toggle_nvda():
        '''Toggles NVDA on and off'''
        if not actions.user.is_nvda_running():
            actions.key("ctrl-alt-n") 
            actions.user.tts("Turning NVDA on")
        elif actions.user.is_nvda_running():
            actions.user.with_nvda_mod_press('q')
            actions.user.tts("Turning NVDA off")
            time.sleep(1)
            actions.key("enter")



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
        NVDA_RUNNING_CONSTANT = 0
        return True if nvda_client.nvdaController_testIfRunning() == NVDA_RUNNING_CONSTANT else False
    
    def nvda_tts(text: str, use_clipboard: bool= False):
        '''text to speech with NVDA'''



ctxWindowsNVDARunning = Context()
ctxWindowsNVDARunning.matches = r"""
os: windows
tag: user.nvda_running
"""

@ctxWindowsNVDARunning.action_class('user')
class UserActions:

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
    
    def tts(text: str):
        """Text to speech"""
        if settings.get("user.tts_via_screenreader"):
            actions.user.nvda_tts(text)
        else:
            actions.user.base_win_tts(text)


    def cancel_current_speaker():
        """Cancel the narrator tts from NVDA"""
        nvda_client.nvdaController_cancelSpeech()

    def braille(text: str):
        """Output braille with NVDA"""
        nvda_client.nvdaController_brailleMessage(text)



# Not sure how to usually have speak words on
# since if we have it on all the time then it will mess 
# def toggle_speak_typed_words(_):
#     """Toggles the speak typed words setting"""
#     actions.user.with_nvda_mod_press("3")

# speech_system.register("pre:phrase", toggle_speak_typed_words)
# speech_system.register("post:phrase", toggle_speak_typed_words)

