from talon import registry, Module, actions
from ..lib.HTMLbuilder import Builder
import html, re

mod = Module()

def remove_wrapper(text: str):
	if text.startswith("Context("):
		text = text.replace("Context(", "", 1)  # Remove the first occurrence of "Context("
		text = text.rstrip(")") 
		return text
	
	regex = r"[^\"']+[\"']([^\"']+)[\"']"
	match = re.search(regex, text)
	return match.group(1) if match else None


@mod.action_class
class Actions:
	
	def get_active_commands():
		"""Returns a list of all commands"""
		command_dict = {}
		for ctx in registry.active_contexts():

			phrases = [remove_wrapper(str(command.rule))
			  for command in ctx.commands.values()]


			code = [remove_wrapper(str(command.script)
					   )
					for command in 
					ctx.commands.values()
				]
			
			ctx_name = remove_wrapper(str(ctx)) 

			command_dict[ctx_name] = {
				"phrases": phrases,
				# "line_numbers": line_numbers,
				"code": code
			}	
		return command_dict

	def open_command_list():
		"""Opens the command list"""
		commands_list = actions.user.get_active_commands()
		builder = Builder()
		builder.title("All Currently Active Talon Commands")
		for ctx in commands_list:

			phrases = commands_list[ctx]["phrases"]
			# line_numbers = commands_list[ctx]["line_numbers"]
			fns = commands_list[ctx]["code"]

			if len(phrases) == 0:
				continue

			builder.h1(ctx)
			builder.start_table(["Command Phrase", "Code"])  # Removed extra comma
			for phrase, code in zip(phrases, fns):
				builder.add_row([phrase, code])
			builder.end_table()
		builder.render()
