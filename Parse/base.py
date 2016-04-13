from abc import abstractmethod, ABCMeta

from base_class import BaseClass


class BaseParser(BaseClass, metaclass=ABCMeta):
	@abstractmethod
	def parse (self, response, url: str):
		pass
