from talon import actions, Module, settings

mod = Module()

mod.setting(
    "nvda_key",
    type=str,
    default="capslock",
    desc="The key that is used as the NVDA key",
)


@mod.action_class
class Actions:
    def with_nvda_key(key: str):
        """Presses the NVDA key"""
        nvda_key = settings.get("user.nvda_key")
        actions.key(f'{nvda_key}:down') 
        actions.key(key)
        actions.key(f'{nvda_key}:up')