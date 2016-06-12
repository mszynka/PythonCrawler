import unittest
from unittest import TestCase

from Mediator.mediator import Mediator
from Tests.Mocks import Mock


class TestMediator(TestCase):
	def setUp (self):
		self.url = Mock.url()
		seed = list()
		seed.append(self.url)
		self.mediator = Mediator(seed, 1)

	def test_get_url (self):
		url = self.mediator.get_url()

		self.assertEqual(url, self.url)

	@unittest.skipIf(Mock.hasSingleUrl, "Url container in mediator is a dict so adding 5 equal elements is "
	                                    "pointless")
	def test_push_urls (self):
		urls = Mock.urls_unique(5)

		self.mediator.push_urls(urls)

		self.assertGreaterEqual(len(self.mediator._urls.keys()), 5)

	def test_push_models (self):
		counter = 0
		max = 15

		for i in range(5, max):
			with self.subTest(i=i):
				models = Mock.models(i)
				counter += i

				self.mediator.push_models(models)
				# FIX: dynamically get class name
				count = self.mediator._model_queue.qsize()

				self.assertEqual(counter, count)

	def test_get_models (self):
		models = Mock.models(5)

		self.mediator.push_models(models)
		test = self.mediator.get_models()

		self.assertEqual(len(models), len(test))

	def test_push_response (self):
		response = Mock.response()

		self.mediator.push_response(response)

		self.assertEqual(self.mediator._response_queue.qsize(), 1)
		self.assertEqual(self.mediator._response_queue.get(), response)

	def test_push_responses (self):
		responses = Mock.responses(5)

		self.mediator.push_responses(responses)

		self.assertEqual(self.mediator._response_queue.qsize(), len(responses))
		for response in responses:
			self.assertEqual(self.mediator._response_queue.get(), response)

	def test_get_responses (self):
		response = Mock.response()
		self.mediator.push_response(response)

		responses = self.mediator.get_responses()

		self.assertEqual(len(responses), 1)
		self.assertEqual(responses.first(), response)

	def test_keep_workers (self):
		value = not (self.mediator.keep_crawler() and self.mediator.keep_parser() and self.mediator.keep_database())

		self.assertEqual(self.mediator.keep_workers(), value)

	def test_keep_crawler (self):
		self.mediator._urls_get = 60
		self.mediator._urls_set = 50

		self.assertFalse(self.mediator.keep_crawler())

		self.mediator._urls_get = 40
		self.mediator._urls_set = 40

		self.assertTrue(self.mediator.keep_crawler())

	def test_keep_parser (self):
		self.assertEqual(self.mediator.keep_crawler(), self.mediator.keep_parser())

	def test_keep_database (self):
		self.assertEqual(self.mediator.keep_crawler(), self.mediator.keep_database())
