import os, configparser
from talon import actions, Module, Context

PATH = os.path.expanduser("~\\AppData\\Roaming\\nvda\\nvda.ini")

"""
Read in and parse the nvda.ini file, then write back to it.
We need to skip the first line of the file, which is a schema version
and would otherwise cause the configparser to fail since it isn't valid ini
"""


mod = Module()
@mod.action_class
class Actions:
    def nvda_set_setting(setting: str, value: bool):
        """Sets an NVDA setting to a given value"""

ctx = Context()
ctx.matches = r"""
os: windows
"""

@ctx.action_class("user")
class UserActions:
    def nvda_set_setting(setting: str, value: bool):

        # Load the nvda.ini file, skipping the first line
        with open(PATH, 'r') as f:
            next(f)  # Skip the first line
            config_string = f.read()

        config = configparser.RawConfigParser()
        config.optionxform = str
        config.read_string(config_string)

        # Search for the speakTypedWords setting in all sections
        for section in config.sections():
            if setting in config[section]:
                config[section][setting] = str(value)

        # Save the changes back to the nvda.ini file, preserving the first line
        with open(PATH, 'r') as f:
            first_line = next(f)  # Save the first line

        with open(PATH, 'w') as configfile:
            configfile.write(first_line)  # Write the first line back to the file
            config.write(configfile)  # Write the rest of the config
        print(f"Set NVDA setting: {setting} to {value}")
        actions.user.with_nvda_mod_press("ctrl-r")