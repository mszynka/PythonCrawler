from unittest import TestCase

from Crawl.crawler import Crawler
from Parse.response import Response
from Tests.Mocks import Mock


class TestCrawler(TestCase):
	def setUp (self):
		self.crawler = Crawler()

	def test_execute_request_instance (self):
		response = self.crawler.execute_request(Mock.url())

		self.assertIsInstance(response, Response)

	def test_execute_request_contents (self):
		response = self.crawler.execute_request(Mock.url())

		self.assertIsNotNone(response.html)

	def test_execute_request_url (self):
		url = Mock.url()
		response = self.crawler.execute_request(url)

		self.assertEqual(response.url, url)
