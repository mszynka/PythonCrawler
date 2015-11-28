class LinkContainerException(Exception):
	def __init__ (self, message=None, container=None, externalException=None):
		self.container = container
		self.message = message
		self.externalException = externalException

	def __str__ (self):
		if not self.message or self.message == "":
			self.message = "Undefined LinkContainerException"

		if self.container and self.externalException:
			return str.join("\n", [str(self.message), str(self.container), str(self.externalException)])
		elif self.container:
			return str.join("\n", [str(self.message), str(self.container)])
		elif self.externalException:
			return str.join("\n", [str(self.message), str(self.externalException)])
		else:
			return "Undefined LinkContainerException"
