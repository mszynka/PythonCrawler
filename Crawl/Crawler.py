"""
-------------------
	Web crawler
-------------------
	Credits: http://www.netinstructions.com/how-to-make-a-web-crawler-in-under-50-lines-of-python-code/
"""

import sys
import urllib
from threading import Thread
from urllib.parse import urlparse

from crawler.LinkParser import LinkParser


def tokenize_links (links):
	"""
	Link tokenizer for smart management
	:param links: Links array or string
	:return: Parsed links dict
	"""
	# TODO: remove this function
	outputLinksDict = dict()

	if isinstance(links, list):
		# Debug.log("LinkAnalyzer found list of links", Debug.Severity.DebugInfo)
		for link in links:
			tmp_url = urlparse(link)
			if tmp_url.path != '':
				if tmp_url.netloc in outputLinksDict:
					outputLinksDict[tmp_url.netloc].append({ tmp_url.path: False })
				else:
					outputLinksDict[tmp_url.netloc] = [{ tmp_url.path: False }]
			else:
				outputLinksDict[tmp_url.netloc] = [{ "/": False }]
		return outputLinksDict
	elif isinstance(links, str):
		# Debug.log("LinkAnalyzer found single link", Debug.Severity.DebugInfo)
		tmp_url = urlparse(links)
		if tmp_url.path != '':
			outputLinksDict[tmp_url.netloc] = [{ tmp_url.path: False }]
		else:
			outputLinksDict[tmp_url.netloc] = [{ "/": False }]
		return outputLinksDict

class Crawler(Thread):
	def __init__ (self):
		super().__init__()
		self._parser = LinkParser()  # Parser initialization
		self._pagesVisited = []  # List of already visited links
		self._pagesToVisit = { }  # Dict of pages to crawl

	def crawl (self, url):
		"""
				Crawler crawling method
				:param url: base url to start crawling with
				:return: boolean upon success/failure
			"""
		self._pagesToVisit = tokenize_links(url)  # Crawler page's links array

		print(self._pagesToVisit)
		url = "http://" + str(list(self._pagesToVisit.keys())[0])
		self._pagesVisited.append(url)
		# self._pagesToVisit = self._pagesToVisit[1:]
		# noinspection PyBroadException
		try:
			# Debug.log(str.join(" ", [len(self._pagesVisited), " Visiting: ", url]), Debug.Severity.DebugInfo)
			data, links = self._parser.get_links(url)
			print(data)
			self._pagesToVisit += links
		except urllib.error.HTTPError as e:
			# Debug.log(str.join(" ", [str(e.code), str(e.reason)]), Debug.Severity.Warning)
			return e.code
		except:
			print(sys.exc_info())
			return False

		# Debug.log(str.join(" ", ["Visited", str(len(self._pagesVisited)), "pages"]), Debug.Severity.Info)
		return True
