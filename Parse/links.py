"""
----------------------
  Link parser module
----------------------
"""
from urllib.parse import urlparse

from pyquery import PyQuery

from Parse.base import BaseParser
from Parse.response import Response


class LinkParser(BaseParser):
	# noinspection PyAttributeOutsideInit
	def parse (self, response: Response):
		self._response = response
		self._parse_links()
		self._fix_links()

		return self._links

	def _parse_links (self):
		pq_parser = PyQuery(self._response.html)
		self._links = [x.attrib["href"] for x in pq_parser("a[href]")]

	def _fix_links (self):
		self._get_host_name()
		self._prepend_links_with_hostname()

	def _get_host_name (self):
		p_url = urlparse(self._response.url)
		self.hostname = str.format("{0}://{1}", p_url.scheme, p_url.netloc)

	def _prepend_links_with_hostname (self):
		for iterator in range(0, len(self._links)):
			if self._links[iterator][0] == "/":
				# noinspection PyUnusedLocal
				self._links[iterator] = str.format("{0}{1}", self.hostname, self._links[iterator])
