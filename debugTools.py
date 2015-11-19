from enum import Enum


class Debug:
	DebugLevel = 4

	@staticmethod
	def log(message):
		print(message)

	@staticmethod
	def log(message, severity):
		if isinstance(severity, Debug.Severity) and severity.value <= Debug.DebugLevel:
			Debug.log(str.join(" ", [severity.__str__, ":::", message]))

	class Severity(Enum):
		DebugInfo = 4
		Info = 3
		Warning = 2
		Error = 1

		@property
		def __str__(self):
			if self.value == 4:
				return "Debug"
			elif self.value == 3:
				return "Info"
			elif self.value == 2:
				return "Warning"
			elif self.value == 1:
				return "Error"
			else:
				raise ValueError("Debug.Severity value does not contain itself!")

#TODO: tests
#TODO: docs
#TODO: progressbar
'''
PROGRESSBAR SCAFFOLDS
import click

with click.progressbar(range(1000000)) as bar:
    for i in bar:
        pass
'''
