import enum
from typing import Any, List, Literal, Optional, TypedDict

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

    @staticmethod
    def generate_from(value: str):
        for member in ServerStatusResult:
            if member.value == value:
                return member
        raise KeyError(f"Invalid status result: {value}")


class IPCServerResponse(TypedDict):
    processedCommands: List[str]
    returnedValues: List[Any]
    statusResults: List[ServerStatusResult]


class IPCClientResponse(enum.Enum):
    NO_RESPONSE = "noResponse"
    TIMED_OUT = "timedOut"
    GENERAL_ERROR = "generalError"
    SUCCESS = "success"


class ResponseBundle(TypedDict):
    client: IPCClientResponse
    server: Optional[None | IPCServerResponse]
