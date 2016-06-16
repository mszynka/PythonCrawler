from unittest import TestCase

from bs4 import BeautifulSoup

from Database.models import Models
from Parse.links import LinkParser
from Parse.parser import Parser
from Parse.response import Response
from Tests.Mocks import Mock


class TestParser(TestCase):
	def setUp (self):
		self.parser = Parser()

	def test_parse (self):
		response = Mock.response()
		lp = LinkParser()
		encoding = response.html.info().get_charset()
		soup_string = BeautifulSoup(response.html.read(), "lxml", from_encoding=encoding)
		decoded_response = Response(response.url, soup_string.decode())
		url_count = len(lp.parse(response))

		models, links = self.parser.parse(response)

		self.assertIsInstance(links, list)
		self.assertEqual(len(links), url_count)
		self.assertIsInstance(models, Models)
		self.assertGreaterEqual(len(models), 0)
