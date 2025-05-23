from typing import Literal

from talon import Module

mod = Module()

mod.setting(
    "tts_speed",
    type=float,
    default=8,
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
    default=True,
    desc="If true, plays back dictation with text to speech through the screenreader, not within Talon",
)

mod.setting(
    "echo_braille",
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
    "echo_dictation",
    type=bool,
    default=True,
    desc="If nonzero, plays back dictation with text to speech",
)

mod.setting(
    "start_screenreader_on_startup",
    type=bool,
    default=False,
    desc="If True, starts the screenreader on Talon startup",
)

mod.setting(
    "nvda_key",
    type=str,
    default="capslock",
    desc="The key that is used as the NVDA key",
)

mod.setting(
    "jaws_key",
    type=str,
    default="insert",
    desc="The key that is used as the JAWS key",
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
    default=80,
    desc="The volume of the text to speech",
)


mod.setting(
    "disable_keypresses",
    type=bool,
    default=False,
    desc="If True, disables all keypresses to prevent accidental keypresses",
)

mod.setting(
    "sound_on_keypress",
    type=bool,
    default=False,
    desc="If True, plays a sound on every keypress to help prevent accidental keypresses",
)


mod.setting(
    "orca_key",
    type=str,
    default="capslock",
    desc="The key that is used as the Orca modifier key",
)

mod.setting("announce_mode_updates", type=bool, default=True)

mod.setting("addon_debug", type=bool, default=False)

mod.tag("sightFreeTalonInstalled", desc="Tag to indicate that you can use TTS")

# mod.mode("strict_dictation", desc="Dictation mode with only a subset of dictation commands")
# mod.mode('strict_command', desc='Command mode with only a subset of command commands')
