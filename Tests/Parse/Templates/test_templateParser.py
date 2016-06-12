from unittest import TestCase

from Database.models import Models
from Parse.Templates.TemplateParser import TemplateParser
from Tests.Mocks import Mock


class TestTemplateParser(TestCase):
	def setUp (self):
		self.template_parser = TemplateParser()

	def test_parse (self):
		response = Mock.response()
		template = Mock.template(response.url)

		models = self.template_parser.parse(response.html, template)

		self.assertIsNotNone(models)
		self.assertIsInstance(models, Models)
		self.assertGreaterEqual(len(models), 0)
