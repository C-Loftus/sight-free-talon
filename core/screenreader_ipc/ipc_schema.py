import enum
from typing import List, Literal, Dict, Any, TypedDict

# Exhaustive list of commands that can be sent to the NVDA addon server

IPC_COMMAND = Literal[
    "disableSpeechInterruptForCharacters",
    "enableSpeechInterruptForCharacters",
    "getSpeechInterruptForCharacters",
    "disableSpeakTypedWords",
    "enableSpeakTypedWords",
    "getSpeakTypedWords",
    "disableSpeakTypedCharacters",
    "enableSpeakTypedCharacters",
    "getSpeakTypedCharacters",
    "debug",
]


class ServerSpec(TypedDict):
    address: str
    port: str
    valid_commands: List[IPC_COMMAND]


class ServerStatusResult(enum.Enum):
    SUCCESS = "success"
    INTERNAL_SERVER_ERROR = "serverError"
    INVALID_COMMAND_ERROR = "commandError"
    RUNTIME_ERROR = "runtimeError"
    JSON_ENCODE_ERROR = "jsonEncodeError"


class IPCServerResponse(TypedDict):
    processedCommands: List[str]
    returnedValues: List[Any]
    statusResults: List[ServerStatusResult]


class IPCClientResponse(enum.Enum):
    NO_RESPONSE = "noResponse"
    TIMED_OUT = "timedOut"
    GENERAL_ERROR = "generalError"
    SUCCESS = "success"


RETURNED_VAL = any | None
