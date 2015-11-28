class LinkContainerException(Exception):
	def __init__ (self, message=None, container=None, externalException=None):
		self.__container = container
		self.__message = message
		self.__externalException = externalException

	def __str__ (self):
		if not self.__message or self.__message == "":
			self.__message = "Undefined LinkContainerException"

		if self.__container and self.__externalException:
			return str.join("\n", [str(self.__message), str(self.__container), str(self.__externalException)])
		elif self.__container:
			return str.join("\n", [str(self.__message), str(self.__container)])
		elif self.__externalException:
			return str.join("\n", [str(self.__message), str(self.__externalException)])
		else:
			return self.__message
