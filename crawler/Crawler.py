"""
-------------------
	Web crawler
-------------------
	Credits: http://www.netinstructions.com/how-to-make-a-web-crawler-in-under-50-lines-of-python-code/
"""

import sys
import urllib
from threading import Thread

from analytics.LinkAnalyzer import LinkAnalyzer
from crawler.LinkParser import LinkParser
from debugTools import Debug


class Crawler:
	class CrawlerWorker(Thread):
		def tool (self):
			pass

	def __init__ (self):
		self._parser = LinkParser()  # Parser initialization
		self._pagesVisited = []  # List of already visited links
		self._pagesToVisit = { }  # Dict of pages to crawl

	def crawl (self, url, maxPages):
		"""
				Crawler crawling method
				:param url: base url to start crawling with
				:param maxPages: maximum pages to crawl (link order defines the sequence)
				:return: boolean upon success/failure
			"""
		self._pagesToVisit = LinkAnalyzer.tokenize_links(url)  # Crawler page's links array

		while len(self._pagesVisited) < maxPages and len(self._pagesToVisit):
			url = self._pagesToVisit[0].geturl()
			self._pagesVisited.append(url)
			self._pagesToVisit = self._pagesToVisit[1:]
			try:
				Debug.log(str.join(" ", [len(self._pagesVisited), " Visiting: ", url]), Debug.Severity.DebugInfo)
				data, links = self._parser.get_links(url)
				# if data.find(word) > -1:
				self._pagesToVisit += links
			except urllib.error.HTTPError as e:
				Debug.log(str.join(" ", [str(e.code), str(e.reason)]), Debug.Severity.Warning)
				return e.code
			except:
				Debug.log(str.join(" ", [str(sys.exc_info()[0])]), Debug.Severity.Warning)

		Debug.log(str.join(" ", ["Visited", len(self._pagesVisited), "pages"]), Debug.Severity.Info)
		return True
