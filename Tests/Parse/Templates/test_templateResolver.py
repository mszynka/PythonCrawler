from unittest import TestCase

from Parse.Templates.TemplateResolver import TemplateResolver
from Tests.Mocks import Mock


class TestTemplateResolver(TestCase):
	def setUp (self):
		self.template_resolver = TemplateResolver("Parse/Templates/spiewnik.xml")

	def test_resolve (self):
		url = Mock.url()

		template = self.template_resolver.resolve(url)

		self.assertIsNotNone(template)
