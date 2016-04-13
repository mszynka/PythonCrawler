from pyquery import PyQuery

from Database.model import ParsedObject
from Parse.base import BaseParser


class ContentParser(BaseParser):
	# TODO: Response class
	def parse (self, response, url: str):
		# TODO: Invent another parsing method
		# TODO: Template resolver etc
		pq_parser = PyQuery(response)

		site_main = pq_parser('div.site-main')
		content = site_main('.entry-content')
		pheader = site_main('.entry-header')
		pbody = content('pre:first')
		pchords = content('p + pre')

		return ParsedObject(header=pheader.text(), body=pbody.text(), chords=pchords.text(), url=url)
