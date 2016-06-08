from Parse.Templates.TemplateManager import TemplateManager
from Parse.base import BaseParser
from Parse.response import Response


class ContentParser(BaseParser):
	def __init__ (self):
		super().__init__()
		self.template_manager = TemplateManager()

	def parse (self, response: Response):
		return self.template_manager.parse(response)
