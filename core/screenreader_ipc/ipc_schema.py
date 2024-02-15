from typing import Literal

# Exhaustive list of commands that can be sent to the NVDA addon server
IPC_COMMAND = Literal[
    "disableSpeechInterruptForCharacters",
    "enableSpeechInterruptForCharacters",
    "disableSpeakTypedWords",
    "enableSpeakTypedWords",
    "disableSpeakTypedCharacters",
    "enableSpeakTypedCharacters",
    "debug"
]