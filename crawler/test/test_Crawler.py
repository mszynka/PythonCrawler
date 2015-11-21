from unittest import TestCase

from crawler.Crawler import test_crawler


class TestCrawler(TestCase):
	def test_test_crawler_has_exited_properly(self):
		self.assertTrue(test_crawler("http://getbootstrap.com", "docs", 10))