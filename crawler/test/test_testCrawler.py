from unittest import TestCase
from crawler.crawl import test_crawler

class TestTestCrawler(TestCase):
	def test_test_crawler_has_exited_properly(self):
		self.assertTrue(test_crawler("http://getbootstrap.com", "docs", 10))