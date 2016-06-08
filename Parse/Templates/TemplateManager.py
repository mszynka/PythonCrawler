from Base.base_class import BaseClass
from Parse.Templates.TemplateParser import TemplateParser
from Parse.Templates.TemplateResolver import TemplateResolver

__author__ = 'robin'


class TemplateManager(BaseClass):
	def __init__ (self):
		super().__init__()
		self.xml = 'Parse/Templates/spiewnik.xml'
		self.TResolver = TemplateResolver(self.xml)
		self.TemplateParser = TemplateParser()

	def parse (self, response):
		try:
			template = self.TResolver.resolve(response.url)
			models = self.TemplateParser.parse(response.html, template)
			return models
		except ResourceWarning as w:
			self.logger.warning(w)
			return None
