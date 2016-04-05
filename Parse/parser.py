"""
----------------------
	Parser module
----------------------
"""
from bs4 import BeautifulSoup

from Parse.base import BaseParser

# noinspection PyBroadException
from Parse.content import ContentParser
from Parse.links import LinkParser


class Parser(BaseParser):
	def __init__ (self):
		self._content_p = ContentParser()
		self._link_p = LinkParser()
		super().__init__()

	def parse (self, response, url):
		"""
		Parses response from urlopen
		:param response: urrlib.request.urlopen product
		:param url: URL for logger.purposes
		:returns: Model
		"""
		encoding = response.info().get_charset()
		soup_string = BeautifulSoup(response.read(), "lxml", from_encoding=encoding)
		decoded_response = soup_string.decode()

		self.logger.debug("Initialized parsing")
		# noinspection PyBroadException
		try:
			links = self._link_p.parse(decoded_response, url)
			model = self._content_p.parse(decoded_response, url)
			self.logger.debug("Parsing successful")
			return model, links
		except:
			self.logger.error("Parsing was unsuccessful")
