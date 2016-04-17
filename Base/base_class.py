import logging
from abc import ABCMeta


class BaseClass(metaclass=ABCMeta):
	def __init__ (self):
		self.logger = logging.getLogger(type(self).__name__)
