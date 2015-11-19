from html.parser import HTMLParser
from urllib import parse
import urllib
from urllib.request import urlopen


class LinkParser(HTMLParser):
	def handle_starttag(self, tag, attributes):
		"""
			handle_starttag - overrides HTMLParser handle_starttag searching for links in a[href] HTML tags
			:param:
				tag: HTML tag
				attributes: HTML tag attributes
		"""
		if tag == 'a':
			for (key, value) in attributes:
				if key == 'href':
					newUrl = parse.urljoin(self.baseUrl, value)
					self.links = self.links + [newUrl]

	def get_links(self, url):
		"""
			Crawler content extraction method
			:param url: Base url to start crawling from
			:return:
				htmlString: current page contents as HTML String
				links[]: extracted list of links from HTML content
		"""
		self.links = []  # HTMLParser links array
		self.baseUrl = url  # HTMLParser base url

		request = urllib.request.Request(url, headers={'User-Agent': 'Wget/1.9.1'})  # User-Agent hack for getting
		# content out of non accessible for robots sites
		response = urlopen(request)

		if response.info().get('Content-Type').find('text/html') > -1:
			htmlBytes = response.read()
			htmlString = htmlBytes.decode("utf-8")
			self.feed(htmlString)
			return htmlString, self.links
		else:
			return "", []
