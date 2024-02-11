# import dataclasses
from typing import Literal, Optional, Union

# import json

IPC_COMMAND = Literal[
    "disableSpeechInterruptForCharacters",
    "enableSpeechInterruptForCharacters",
    "disableSpeakTypedWords",
    "enableSpeakTypedWords",
    "disableSpeakTypedCharacters",
    "enableSpeakTypedCharacters" "debug",
]

# @dataclasses.dataclass
# class IPC_Setting_Change:
#     setting_name: str
#     setting_value: Union[str, int, float, bool]

#     def validate(self):
#         if not isinstance(self.setting_name, str):
#             raise TypeError(f"Invalid setting name type: {type(self.setting_name)}")
#         if not isinstance(self.setting_value, (str, int, float, bool)):
#             raise TypeError(f"Invalid setting value type: {type(self.setting_value)}")

# @dataclasses.dataclass
# class IPC_Action:
#     action_name: str
#     action_args: Optional[list[str]]

#     def validate(self):
#         if not isinstance(self.action_name, str):
#             raise TypeError(f"Invalid action name type: {type(self.action_name)}")
#         if self.action_args is not None and not isinstance(self.action_args, list):
#             raise TypeError(f"Invalid action args type: {type(self.action_args)}")

# class IPC_Payload
#     def __init__(self, commands: list[Union[IPC_Setting_Change, IPC_Action]]):
#         self.commands = commands

#     def validate(self):
#         for command in self.commands:
#             if not isinstance(command, (IPC_Setting_Change, IPC_Action)):
#                 raise TypeError(f"Invalid command type: {type(command)}")

#     def serialize(self):
#         return json.dumps([dataclasses.asdict(command) for command in self.commands])
