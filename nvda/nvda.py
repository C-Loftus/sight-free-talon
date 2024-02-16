from talon import actions, Module, settings, cron, Context, clip, speech_system, scope 
import os, ctypes, time  

mod = Module()
ctx = Context()

mod.tag("nvda_running", desc="If set, NVDA is running")

@mod.scope
def set_nvda_running_tag():
    '''Update tags based on if NVDA is running'''
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
    
    def restart_nvda(): 
        """Restarts NVDA"""
        if actions.user.is_nvda_running():
            actions.user.with_nvda_mod_press('q')
            time.sleep(0.5)
            actions.key("down")
            time.sleep(0.5)
            actions.key("enter")
            actions.user.tts("Restarting NVDA")


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
        if os.name != 'nt' or not nvda_client:
            return False
        
        NVDA_RUNNING_CONSTANT = 0
        client_response = nvda_client.nvdaController_testIfRunning()

        if client_response == NVDA_RUNNING_CONSTANT:
            return True
        else:
            if settings.get("user.addon_debug"):
                print(f"NVDA not running. Client response value: {client_response}") 
            return False

    
    def nvda_tts(text: str, use_clipboard: bool= False):
        '''text to speech with NVDA'''

    def test_controller_client():
        """Tests the NVDA controller client"""
        actions.user.tts(f"Controller client value is: {nvda_client.nvdaController_testIfRunning()}")

    def test_reader_addon():
        """Tests the reader addon"""
        actions.user.send_ipc_command("debug")

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
    
    def tts(text: str, interrupt:bool =True):
        """Text to speech within NVDA"""
        if settings.get("user.tts_via_screenreader"):
        # we ignore interrupt since that is done by NVDA
            actions.user.nvda_tts(text)
        else:
            actions.user.base_win_tts(text, interrupt)


    def cancel_current_speaker():
        """Cancel the narrator tts from NVDA"""
        nvda_client.nvdaController_cancelSpeech()

    def braille(text: str):
        """Output braille with NVDA"""
        nvda_client.nvdaController_brailleMessage(text)


def _ready_to_send_ipc():
    SLEEP_MODE = 'sleep' in scope.get("mode")
    SPEC_FILE = os.path.expanduser("~\\AppData\\Roaming\\nvda\\talon_server_spec.json")
    return actions.user.is_nvda_running() and not SLEEP_MODE and os.path.exists(SPEC_FILE)
    

# By default the screen reader will allow you to press a key and interrupt the ph
# rase however this does not work alongside typing given the fact that we are pres
# sing keys.  so we need to temporally disable it then re enable it at the end of 
# the phrase
def disable_interrupt(_):
    if not _ready_to_send_ipc():
        return
    
    # bundle the commands into a single messge
    commands = ["disableSpeechInterruptForCharacters",
                "disableSpeakTypedWords",
                "disableSpeakTypedCharacters"
                ]
    actions.user.send_ipc_commands(commands)

def restore_interrupt_setting(_):
    if not _ready_to_send_ipc():
        return
    
    # bundle the commands into a single message
    commands = ["enableSpeechInterruptForCharacters",
                "enableSpeakTypedWords",
                "enableSpeakTypedCharacters"
                ]
    
    #  this is kind of a hack since we don't know exactly when to re enable it
    #  because we don't have a callback at the end of the last keypress
    update = lambda: actions.user.send_ipc_commands(commands)
    cron.after("1s", update)

if os.name == 'nt':
    speech_system.register("pre:phrase", disable_interrupt)
    speech_system.register("post:phrase", restore_interrupt_setting)
    

