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
from crawler.Links.LinkParser import LinkParser
from debugTools import Debug


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
		self._pagesToVisit = LinkAnalyzer.tokenize_links(url)  # Crawler page's links array

		print(self._pagesToVisit)
		url = "http://" + str(list(self._pagesToVisit.keys())[0])
		self._pagesVisited.append(url)
		# self._pagesToVisit = self._pagesToVisit[1:]
		try:
			Debug.log(str.join(" ", [len(self._pagesVisited), " Visiting: ", url]), Debug.Severity.DebugInfo)
			data, links = self._parser.get_links(url)
			print(data)
			self._pagesToVisit += links
		except urllib.error.HTTPError as e:
			Debug.log(str.join(" ", [str(e.code), str(e.reason)]), Debug.Severity.Warning)
			return e.code
		except:
			print(sys.exc_info())
			return False

		Debug.log(str.join(" ", ["Visited", str(len(self._pagesVisited)), "pages"]), Debug.Severity.Info)
		return True
