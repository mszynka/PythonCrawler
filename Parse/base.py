from abc import abstractmethod, ABCMeta

from Base.base_class import BaseClass
from Parse.response import Response


class BaseParser(BaseClass, metaclass=ABCMeta):
	@abstractmethod
	def parse (self, response: Response):
		pass
