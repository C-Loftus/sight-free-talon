from talon import actions, Module, settings, cron
import os, ctypes


mod = Module()

mod.setting(
    "nvda_key",
    type=str,
    default="capslock",
    desc="The key that is used as the NVDA key",
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
    return {"nvda_running": nvda_running}

# Re-run the above code every 15s to update the scope
cron.interval("15s", check_nvda.update)



@mod.action_class
class Actions:
    def with_nvda_key(key: str):
        """Presses the NVDA key"""
        nvda_key = settings.get("user.nvda_key")
        actions.key(f'{nvda_key}:down') 
        actions.key(key)
        actions.key(f'{nvda_key}:up')