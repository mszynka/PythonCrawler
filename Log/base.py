from abc import abstractmethod, ABCMeta


class BaseLogger(metaclass=ABCMeta):
	def __init__ (self):
		pass

	@abstractmethod
	def configure (self):
		pass
