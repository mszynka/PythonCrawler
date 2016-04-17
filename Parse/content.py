from pyquery import PyQuery

from Database.model import ParsedObject
from Parse.base import BaseParser
from Parse.response import Response


class ContentParser(BaseParser):
	def parse (self, response: Response):
		# TODO: Invent another parsing method
		# TODO: Template resolver etc
		pq_parser = PyQuery(response.html)

		site_main = pq_parser('div.site-main')
		content = site_main('.entry-content')
		pheader = site_main('.entry-header')
		pbody = content('pre:first')
		pchords = content('p + pre')

		return ParsedObject(header=pheader.text(), body=pbody.text(), chords=pchords.text(), url=response.url)
