from unittest import TestCase

from crawler.Links.LinkParser import LinkParser


# TODO: tests
class TestLinkParser(TestCase):
	def test_get_links_not_empty (self):
		link_parser = LinkParser()
		self.assertIsNot(link_parser.get_links("http://getbootstrap.com"), "", [])
