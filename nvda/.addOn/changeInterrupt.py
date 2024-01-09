import globalPluginHandler
from scriptHandler import script
import config

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	@script(gesture="kb:NVDA+9")
	def script_announceNVDAVersion(self, gesture):
		interrupt = config.conf["keyboard"]["speechInterruptForCharacters"]
		config.conf["keyboard"]["speechInterruptForCharacters"] = not interrupt		
        