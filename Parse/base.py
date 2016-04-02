import logging
from abc import abstractmethod, ABCMeta


class BaseParser(metaclass=ABCMeta):
	def __init__ (self):
		self.logger = logging.getLogger(type(self).__name__)

	@abstractmethod
	def parse (self, response, url: str):
		pass
