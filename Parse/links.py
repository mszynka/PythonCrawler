"""
----------------------
  Link parser module
----------------------
"""
from urllib.parse import urlparse

from pyquery import PyQuery

from Parse.base import BaseParser


class LinkParser(BaseParser):
	def parse (self, response, url):
		pq_parser = PyQuery(response)
		links = [x.attrib["href"] for x in pq_parser("a[href]")]

		return self._tokenize_links(links)

	def _tokenize_links (self, links):
		"""
		Link tokenizer for smart management
		:param links: Links array or string
		:return: Parsed links dict
		"""
		# TODO: remove this function
		output_links_dict = dict()

		if isinstance(links, list):
			self.logger.info("Tokenizer found list of links")
			for link in links:
				tmp_url = urlparse(link)
				if tmp_url.path != '':
					if tmp_url.netloc in output_links_dict:
						output_links_dict[tmp_url.netloc].append({ tmp_url.path: False })
					else:
						output_links_dict[tmp_url.netloc] = [{ tmp_url.path: False }]
				else:
					output_links_dict[tmp_url.netloc] = [{ "/": False }]
			return output_links_dict
		elif isinstance(links, str):
			self.logger.info("Tokenizer found single link")
			tmp_url = urlparse(links)
			if tmp_url.path != '':
				output_links_dict[tmp_url.netloc] = [{ tmp_url.path: False }]
			else:
				output_links_dict[tmp_url.netloc] = [{ "/": False }]
			return output_links_dict
