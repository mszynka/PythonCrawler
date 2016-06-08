import re
from xml.dom import minidom

from Base.base_class import BaseClass

__author__ = 'robin'


class TemplateResolver(BaseClass):
	def __init__ (self, xml):
		super().__init__()
		self.Xml = xml
		self.UrlDict = { }
		xmldoc = minidom.parse(xml)
		for site in xmldoc.getElementsByTagName('site'):
			listamoja = []
			for concept in site.getElementsByTagName('concept'):
				li = [{ obj.attributes['name'].value: obj.attributes['query'].value } for obj in
				      concept.getElementsByTagName('object')]
				la = { concept.attributes['name'].value: li }
				listamoja.extend([la])
			self.UrlDict[site.attributes['url'].value] = listamoja

	def resolve (self, url):
		for a in sorted(self.UrlDict, reverse=True):
			if re.match(r'^' + a + '(\D*\d*\D*\d*)*$', url):
				return self.UrlDict[a]

		raise ResourceWarning()
