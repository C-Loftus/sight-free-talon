from talon import actions, Module, settings, cron, Context, clip, registry
import os, ctypes


mod = Module()
ctx = Context()

mod.tag("nvda_running", desc="NVDA is running")

mod.setting(
    "nvda_key",
    type=str,
    default="capslock",
    desc="The key that is used as the NVDA key",
)

mod.setting(
    "tts_via_screenreader",
    type=bool,
    default=False,
    desc="If true, plays back dictation with text to speech through the screenreader, not within Talon",
)

@mod.scope
def check_nvda():
    '''Check if NVDA is running'''
    # Check if it is running without spawning a thread or process
    def is_nvda_running():
        try:
            hwnd = ctypes.windll.user32.FindWindowW(None, "NVDA")
            return hwnd != 0
        except Exception as e:
            print(f"Error: {e}")
            return False

    nvda_running = is_nvda_running()
    if nvda_running:
        ctx.tags = ["user.nvda_running"]
    else:
        ctx.tags = []

# Re-run the above code every 15s to update the scope
cron.interval("3s", check_nvda.update)


# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2023 NV Access Limited, Łukasz Golonka, Leonard de Ruijter
# This file is covered by the GNU Lesser General Public License, version 2.1.
# See the file license.txt for more details.

# Load the NVDA client library
# get dir of this file
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
dll_path = os.path.join(dir_path, "nvdaControllerClient64.dll")

clientLib = ctypes.windll.LoadLibrary(dll_path)

# Test if NVDA is running, and if its not show a message
res = clientLib.nvdaController_testIfRunning()
if res != 0:
	errorMessage = str(ctypes.WinError(res))
	ctypes.windll.user32.MessageBoxW(0, "Error: %s" % errorMessage, "Error communicating with NVDA", 0)
    # actions.user.robot_tts("Error communicating with NVDA")


@mod.action_class
class Actions:
     
    def toggle_nvda():
        '''Toggles NVDA on and off'''
        if not actions.user.is_nvda_running():
            actions.key("ctrl-alt-n") 
            actions.user.robot_tts("NVDA on")
        elif actions.user.is_nvda_running():
            actions.user.with_nvda_mod_press('q')
            actions.user.robot_tts("NVDA off")


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
        return "user.nvda_running" in ctx.tags
    
    def nvda_tts(text: str):
        '''text to speech with NVDA'''

ctxNVDARunning = Context()
ctxNVDARunning.matches = r"""
tag: user.nvda_running
"""

@ctxNVDARunning.action_class("user")
class NVDAActions:
    def nvda_tts(text: str, use_clipboard: bool = False):
        """text to speech with NVDA"""

        # Text can be sent via the clipboard or directly to NVDA using the dll
        if use_clipboard:
            with clip.revert():
                clip.set_text(text) # sets the result to the clipboard
                actions.sleep("50ms")
                actions.user.with_nvda_mod_press('c')
        else:
            clientLib.nvdaController_speakText(text)

    


ctxWindowsNVDARunning = Context()
ctxWindowsNVDARunning.matches = r"""
os: windows
tag: user.nvda_running
"""
@ctxWindowsNVDARunning.action_class('user')
class UserActions:
    
    def robot_tts(text: str):
        """text to speech"""
        
        if settings.get("user.tts_via_screenreader"):
            actions.user.nvda_tts(text)
        else:
            actions.user.windows_robot_tts(text)