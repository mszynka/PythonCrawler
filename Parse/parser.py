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
from Parse.response import Response


class Parser(BaseParser):
	def __init__ (self):
		self._content_p = ContentParser()
		self._link_p = LinkParser()
		super().__init__()

	def parse (self, response: Response):
		"""
		Parses response from urlopen
		:param response: urrlib.request.urlopen product
		:returns: Model
		"""
		encoding = response.html.info().get_charset()
		soup_string = BeautifulSoup(response.html.read(), "lxml", from_encoding=encoding)
		decoded_response = Response(response.url, soup_string.decode())

		self.logger.debug("Initialized parsing")
		# noinspection PyBroadException
		try:
			links = self._link_p.parse(decoded_response)
			model = self._content_p.parse(decoded_response)
			self.logger.debug("Parsing successful")
			return model, links
		except:
			self.logger.error("Parsing was unsuccessful")
			return None, None
