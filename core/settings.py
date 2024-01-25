from talon import Module
from typing import Literal

mod = Module()

mod.setting(
    "tts_speed",
    type=float,
    default=1.0,
    desc="Speed of text to speech",
)

mod.setting(
    "echo_context",
    type=bool,
    default=False,
    desc="If true, plays back dictation with text to speech",
)

mod.setting(
    "tts_via_screenreader",
    type=bool,
    default=False,
    desc="If true, plays back dictation with text to speech through the screenreader, not within Talon",
)

mod.setting(
    "braille_output",
    type=bool,
    default=False,
    desc="If true, outputs braille through your screenreader",
)

ScreenreaderType = Literal["NVDA", "JAWS", "Narrator", "Orca"]
mod.setting(
    "screenreader_type",
    type=ScreenreaderType,
    default="NVDA",
    desc="The screenreader you are using",
)

mod.setting(
    'echo_dictation',
    type = bool,
    default = True,
    desc = 'If nonzero, plays back dictation with text to speech'
)

mod.setting(
    'start_screenreader_on_startup',
    type = bool,
    default = False,
    desc = 'If True, starts the screenreader on Talon startup'
)

mod.setting(
    "nvda_key",
    type=str,
    default="capslock",
    desc="The key that is used as the NVDA key",
)

mod.setting(
    "speak_errors",
    type=bool,
    default=True,
    desc="If True, speaks errors when they occur",
)

# Must be between 1 and 100
mod.setting(
    "tts_volume",
    type=int,
    default=100,
    desc="The volume of the text to speech",
)

mod.setting(
    "enable_break_timer",
    type=bool,
    default=False,
    desc="If True, enables the eyestrain break timer to display a notification every 20 minutes",
)


mod.setting("disable_keypresses", 
    type=bool, 
    default=False, 
    desc="If True, disables all keypresses to prevent accidental keypresses"
)

mod.setting("sound_on_keypress", 
    type=bool,
    default=False, 
    desc="If True, plays a sound on every keypress to help prevent accidental keypresses"
)

mod.setting("min_until_break", 
    type=int,
    default=10
)

mod.setting("orca_key",
    type=str,
    default="capslock",
    desc="The key that is used as the Orca modifier key"
)

mod.setting("announce_mode_updates",
    type=bool,
    default=True
)

mod.setting("addon_debug",
    type=bool,
    default=False
)

# mod.mode("strict_dictation", desc="Dictation mode with only a subset of dictation commands")
# mod.mode('strict_command', desc='Command mode with only a subset of command commands')
