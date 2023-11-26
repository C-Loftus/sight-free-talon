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

ScreenreaderType = Literal["NVDA", "JAWS", "Narrator"]
mod.setting(
    "screenreader_type",
    type=ScreenreaderType,
    default="NVDA",
    desc="The screenreader you are using",
)

mod.setting(
    'user.echo_dictation',
    type = bool,
    default = True,
    desc = 'If nonzero, plays back dictation with text to speech'
)