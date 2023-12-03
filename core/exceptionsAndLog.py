from talon import  actions, registry, resource
from talon_init import TALON_HOME
import os, time
from typing import Optional, Literal


talon_log = os.path.join(TALON_HOME, "talon.log")
if not os.path.exists(talon_log):
    raise Exception("talon.log does not exist")

last_line = None   

caller = resource.watch(talon_log, 'r')
def on_change(_):
    # read the last line of the log file until the last line 
    with open(talon_log, "r") as f:
        global last_line

        initial_output = ""
        final_output = ""
        output_type: Optional[Literal["DEBUG", "ERROR"]] = None

        log = list(reversed(f.readlines()))
        for line in log:
            if line == last_line:
                break

            if "WARNING" in line:
                output_type = "WARNING"
            elif "ERROR" in line:
                output_type = "ERROR"
            elif "DEBUG" in line:
                output_type = "DEBUG"
            
            initial_output = log[0]
            last_line = line

            actions.user.notify(f"{initial_output}\n{final_output}")
            break

caller(on_change)


# # watch the log file for changes
# class LogWatcher:
#     def __init__(self):
#         self.last_size = os.stat(talon_log).st_size
#         self.last_check = time.time()

#     def check(self):
#         if time.time() - self.last_check < 0.5:
#             return
#         self.last_check = time.time()
#         size = os.stat(talon_log).st_size
#         if size == self.last_size:
#             return
#         self.last_size = size
#         self.on_change()

#     def on_change(self):
#         # read the last line of the log file until the first occurence of the word 2023
#         current_year = time.strftime("%Y")
#         with open(talon_log, "r") as f:

#             initial_output = ""
#             final_output = ""
#             output_type: Literal["DEBUG", "ERROR"] = None

#             log = list(reversed(f.readlines()))
#             for line in log:

#                 if current_year in line:
#                     output_type = "DEBUG" if "DEBUG" in line else "ERROR"
                    
#                     initial_output = log[0]
#                     final_output = line
#                     actions.user.notify(f"Log {output_type}:\n{initial_output}\n{final_output}")
#                     break

# log = LogWatcher()
# while True:
#     log.check()
#     time.sleep(0.5)
