from pyquery import PyQuery

from Database.model import ParsedObject
from Parse.base import BaseParser
from Parse.response import Response


class ContentParser(BaseParser):
	def parse (self, response: Response):
		# TODO: Invent another parsing method
		# TODO: Template resolver etc
		pq_parser = PyQuery(response.html)

		site_main = pq_parser('body')
		content = site_main('.post')
		pheader = content('.gridly-copy h2')
		pbody = content('.gridly-copy')
		additional_url = content('.gridly-link')

		return ParsedObject(header=pheader.text(), body=pbody.text(), url=additional_url)
