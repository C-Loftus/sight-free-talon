# from talon import fs, actions
# from talon_init import TALON_HOME
# import os

# talon_log = os.path.join(TALON_HOME, "talon.log")

# if not os.path.exists(talon_log):
#     raise Exception("talon.log does not exist")

# def on_change(path, flags):
#     if flags.exists:
#         print("Log file changed")

# fs.watch(talon_log, on_change)