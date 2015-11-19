"""
-------------------
	Web crawler
-------------------
	Credits: http://www.netinstructions.com/how-to-make-a-web-crawler-in-under-50-lines-of-python-code/
"""

import sys
from html.parser import HTMLParser
from urllib import parse
import urllib
from urllib.request import urlopen
from urllib3.exceptions import HTTPError

from debugTools import Debug


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


# TODO: implement crawling methods (leave analytics to analytics module)
def test_crawler(url, word, maxPages):
	"""
		Crawler temporary test function
		:param:
			url: base url to start crawling with
			word: string you're searching for on urls
			maxPages: maximum pages to crawl (link order defines the sequence)
	"""
	pagesToVisit = [url]  # Crawler page's links array
	numberVisited = 0  # Number of already visited links
	numberFoundWords = 0  # Number of found matching words during crawling

	while numberVisited < maxPages and pagesToVisit != []:
		numberVisited += 1
		url = pagesToVisit[0]
		pagesToVisit = pagesToVisit[1:]
		try:
			Debug.Log(str.join(" ", [numberVisited.__str__(), " Visiting: ", url]), Debug.Severity.DebugInfo)
			parser = LinkParser()
			data, links = parser.get_links(url)
			if data.find(word) > -1:
				numberFoundWords += 1
				pagesToVisit += links
				Debug.Log(" **Success!**", Debug.Severity.Info)
		except HTTPError as e:
			Debug.Log(str.join(" ", [e.code, e.reason]), Debug.Severity.Warning)
			return e.code
		except:
			Debug.Log(str.join(" ", [" **Failed!** ", sys.exc_info()[0]].__str__), Debug.Severity.Warning)

	if numberFoundWords > 0:
		Debug.Log(str.join(" ", ["The word", word, "was found at", url, numberFoundWords.__str__(), "times"]),
		Debug.Severity.Info)
		return True
	else:
		Debug.Log("Word never found", Debug.Severity.Info)
		return False