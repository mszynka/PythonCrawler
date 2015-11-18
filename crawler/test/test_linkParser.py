from unittest import TestCase
from crawler.crawl import LinkParser


class TestLinkParser(TestCase):
	def test_get_links_not_empty(self):
		"""
			Unit test
			Checks if getLinks output is not empty (therefore if there is valid connection)
		"""
		link_parser = LinkParser()
		self.assertIsNot(link_parser.get_links("http://getbootstrap.com"), "",[])