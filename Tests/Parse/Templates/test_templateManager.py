from unittest import TestCase

from Database.models import Models
from Parse.Templates.TemplateManager import TemplateManager
from Tests.Mocks import Mock


class TestTemplateManager(TestCase):
	def setUp (self):
		self.template_manager = TemplateManager()

	def test_parse (self):
		response = Mock.response()

		models = self.template_manager.parse(response)

		self.assertIsNotNone(models)
		self.assertIsInstance(models, Models)
		self.assertGreaterEqual(len(models), 0)
