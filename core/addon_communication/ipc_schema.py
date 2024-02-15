from typing import Literal

# List of all valid commands that can be sent to the screenreader
IPC_COMMAND = Literal[
    # Prevent the screenreader from interrupting echoback
    "disableSpeechInterruptForCharacters",
    "enableSpeechInterruptForCharacters",

    # Prevent the screenreader from interrupting echoback
    "disableSpeakTypedWords",
    "enableSpeakTypedWords",

    # Prevent the screenreader from speaking unnecessary characters in addition to full echo back
    "disableSpeakTypedCharacters",
    "enableSpeakTypedCharacters"

    # Play a sound to confirm that the command was received
    "debug"
]
