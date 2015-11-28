from unittest import TestCase

from crawler.Links.LinkContainerException import LinkContainerException


class TestLinkContainerException(TestCase):
	def test_null_text_message (self):
		exception = LinkContainerException()
		self.assertEqual(str(exception), "Undefined LinkContainerException")

	def test_container (self):
		exception = LinkContainerException(container="Abc")
		self.assertEqual(str(exception), "Undefined LinkContainerException\nAbc")

	def test_externalException (self):
		externalException = ValueError
		exception = LinkContainerException(externalException=externalException)
		self.assertEqual(str(exception), "Undefined LinkContainerException\n" + str(ValueError))
