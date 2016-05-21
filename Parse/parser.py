"""
----------------------
	Parser module
----------------------
"""
from bs4 import BeautifulSoup

from Benchmark.benchmark_data import BenchmarkData
from Benchmark.time_capsule import time_capsule
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
		capsule = time_capsule()
		capsule.start()

		encoding = response.html.info().get_charset()
		soup_string = BeautifulSoup(response.html.read(), "lxml", from_encoding=encoding)
		decoded_response = Response(response.url, soup_string.decode())

		self.logger.debug("Initialized parsing")
		# noinspection PyBroadException
		try:
			links = self._link_p.parse(decoded_response)
			model = self._content_p.parse(decoded_response)
			self.logger.debug("Parsing successful")

			capsule.end()
			data = BenchmarkData.Instance()
			data.appendd(type(self).__name__, self.parse.__name__, capsule.get_time())

			return model, links
		except:
			self.logger.error("Parsing was unsuccessful")
			return None, None
