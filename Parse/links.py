"""
----------------------
  Link parser module
----------------------
"""
import logging
import urllib
from html.parser import HTMLParser
from urllib import parse
from urllib.parse import urlparse
from urllib.request import urlopen

logger = logging.getLogger("LinksParser")


def tokenize_links (links):
	"""
	Link tokenizer for smart management
	:param links: Links array or string
	:return: Parsed links dict
	"""
	# TODO: remove this function
	output_links_dict = dict()

	if isinstance(links, list):
		logger.info("LinkAnalyzer found list of links")
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
		logger.info("LinkAnalyzer found single link")
		tmp_url = urlparse(links)
		if tmp_url.path != '':
			output_links_dict[tmp_url.netloc] = [{ tmp_url.path: False }]
		else:
			output_links_dict[tmp_url.netloc] = [{ "/": False }]
		return output_links_dict


class LinkParser(HTMLParser):
	def __init__ (self):
		super().__init__(convert_charrefs=True)
		self.baseUrl = []
		self.links = []

	def error (self, message):
		pass

	# 	Debug.log(message, Debug.Severity.Error)

	def handle_starttag(self, tag, attributes):
		"""
			handle_starttag - overrides HTMLParser's handle_starttag searching for links in a[href] HTML tags
			:param tag: HTML tag
			:param attributes: HTML tag attributes
		"""
		if tag == 'a':
			for (key, value) in attributes:
				if key == 'href':
					new_url = parse.urljoin(self.baseUrl, value)
					self.links = self.links + [new_url]

	def get_links(self, url):
		"""
			LinkParser content extraction method
			:param url: Base url to start crawling from
			:return html_string: current page contents as HTML String
			:return links[]: extracted list of links from HTML content
		"""
		self.links = []  # HTMLParser links array
		self.baseUrl = url  # HTMLParser base url

		request = urllib.request.Request(url, headers={'User-Agent': 'Wget/1.9.1'})  # User-Agent hack for getting
		# content out of non accessible for robots sites
		response = urlopen(request)

		if response.info().get('Content-Type').find('text/html') > -1:
			html_bytes = response.read()
			html_string = html_bytes.decode("utf-8")  # Detect encoding
			self.feed(html_string)
			return html_string, tokenize_links(self.links)
		else:
			return "", []
