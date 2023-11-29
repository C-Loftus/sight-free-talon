import globalPluginHandler
from scriptHandler import script
import ui
import time, os


relative_path = os.path.join("AppData", "Roaming", "talon", "talon.log")
generic_path = os.path.expanduser(os.path.join("~", relative_path))
talon_log = os.path.expanduser(generic_path)
# read path from talon config fi

# watch the log file for changes
class LogWatcher:
    def __init__(self):
        self.last_size = os.stat(talon_log).st_size
        self.last_check = time.time()

    def check(self):
        if time.time() - self.last_check < 0.5:
            return
        self.last_check = time.time()
        size = os.stat(talon_log).st_size
        if size == self.last_size:
            return
        self.last_size = size
        self.on_change()

    def on_change(self):
        # read the last line of the log file until the first occurence of the word 2023
        current_year = time.strftime("%Y")
        with open(talon_log, "r") as f:

            initial_output = ""
            final_output = ""
            output_type: Literal["DEBUG", "ERROR"] = None

            log = reversed(f.readlines())
            for line in log:

                if current_year in line:
                    output_type = "DEBUG" if "DEBUG" in line else "ERROR"
                    
                    initial_output = log[0]
                    final_output = line

                    break


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	@script(gesture="kb:NVDA+shift+v")
	def script_announceNVDAVersion(self, gesture):
		ui.message(versionInfo.version)