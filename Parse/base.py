from abc import abstractmethod, ABCMeta

from base_class import BaseClass


class BaseParser(BaseClass, metaclass=ABCMeta):
	@abstractmethod
	# TODO: Response class
	def parse (self, response, url: str):
		pass
