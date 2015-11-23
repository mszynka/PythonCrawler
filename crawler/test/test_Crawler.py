from unittest import TestCase

from crawler.Crawler import Crawler


class TestCrawler(TestCase):
	# TODO: tests
	def test_crawler(self):
		c = Crawler()
		self.assertEqual(c.crawl("http://getbootstrap.com", 100), True)
