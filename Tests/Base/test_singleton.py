from unittest import TestCase

from Base.singleton import Singleton


class TestSingleton(TestCase):
	def setUp (self):
		self.value = (lambda: "Some value")
		self.singleton = Singleton(self.value)

	def test_Instance_value (self):
		self.assertEqual(self.singleton.Instance(), self.value())

	def test_Instance_multiple (self):
		one = self.singleton.Instance()
		two = self.singleton.Instance()

		self.assertEqual(one, two)
