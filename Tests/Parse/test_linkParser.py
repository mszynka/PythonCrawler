from unittest import TestCase
from urllib.parse import urlparse

from pyquery import PyQuery

from Parse.links import LinkParser
from Tests.Mocks import Mock


class TestLinkParser(TestCase):
	def setUp (self):
		self.link_parser = LinkParser()

	def test_parse (self):
		response = Mock.response()
		pq_parser = PyQuery(response.html)
		links = list(set([x.attrib["href"] for x in pq_parser("a[href]")]))

		parsed = self.link_parser.parse(response)

		self.assertEqual(len(links), len(parsed))

	def test__parse_links (self):
		response = Mock.response()
		pq_parser = PyQuery(response.html)
		links = [x.attrib["href"] for x in pq_parser("a[href]")]

		parsed = self.link_parser.parse(response)

		self.assertEqual(len(links), len(parsed))

	def test__get_host_name (self):
		url = Mock.url()
		response = Mock.response(url)
		p_url = urlparse(url)
		hostname = str.format("{0}://{1}", p_url.scheme, p_url.netloc)

		self.link_parser._response = response
		self.link_parser._get_host_name()

		self.assertEqual(hostname, self.link_parser.hostname)
