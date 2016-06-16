from unittest import TestCase

from Base.base_iterable import BaseIterable


class TestBaseIterable(TestCase):
	def setUp (self):
		self.container = BaseIterable()

	def tearDown (self):
		self.container.clear()

	def test_append_iter (self):
		self.container.clear()

		string = "An object"
		self.container.append(string)

		for item in self.container:
			self.assertEqual(item, string)

	def test_append_len (self):
		self.container.clear()

		string = "An object"
		self.container.append(string)

		self.assertEqual(len(self.container), 1)

	def test_extend_len (self):
		self.container.clear()

		lst = [1, 2, 3]
		self.container.append(4)
		self.container.extend(lst)

		self.assertEqual(len(self.container), 4)

	def test_clear (self):
		self.container.append(1)

		self.assertGreater(len(self.container), 0)

		self.container.clear()

		self.assertEqual(len(self.container), 0)
