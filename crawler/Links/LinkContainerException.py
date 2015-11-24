class LinkContainerException(Exception):
	def __init__ (self, message=None, container=None):
		self.container = container
		self.message = message

	def __str__ (self):
		if self.message and self.container:
			return str.join("\n", [str(self.message), str(self.container)])
		elif self.message:
			return str(self.message)
		elif self.container:
			return str(self.container)
		else:
			return "Undefined LinkContainerException"
