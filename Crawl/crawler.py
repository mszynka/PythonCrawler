"""
----------------------
	Crawler module
----------------------
"""
import logging
import sys
import time
import urllib
from threading import Thread
from urllib.error import HTTPError
from urllib.request import urlopen

from Parse.links import LinkParser, tokenize_links


class Crawler(Thread):
	def __init__ (self):
		super().__init__()
		self._parser = LinkParser()  # Parser initialization
		self._pagesVisited = list()  # List of already visited links
		self._pagesToVisit = dict()  # Dict of pages to crawl

	def crawl (self, url):
		"""
				Crawler crawling method
				:param url: base url to start crawling with
				:return: boolean upon success/failure
			"""
		self._pagesToVisit = tokenize_links(url)  # Crawler page's links array

		url = "http://" + str(list(self._pagesToVisit.keys())[0])
		logging.info("Crawling: " + url)
		self._pagesVisited.append(url)
		# self._pagesToVisit = self._pagesToVisit[1:]
		# noinspection PyBroadException
		try:
			logging.debug(str.join(" ", [len(self._pagesVisited), " Visiting: ", url]))
			data, links = self._parser.get_links(url)
			self._pagesToVisit += links
		except urllib.error.HTTPError as e:
			logging.debug(str.join(" ", [str(e.code), str(e.reason)]))
			return e.code
		except:
			logging.error(sys.exc_info())
			return False

		logging.info(str.join(" ", ["Visited", str(len(self._pagesVisited)), "pages"]))
		return True

	@staticmethod
	def execute_request (url):
		"""
		Executes a request on given URL
		:param url: URL to get the response
		:returns: urllb.request.urlopen response
		"""
		try:
			request = urllib.request.Request(url, headers={ 'User-Agent': 'Wget/1.9.1' })  # User-Agent hack for getting
			response = urlopen(request)
			logging.debug("Received response %.10s", response)
		except HTTPError as err:
			logging.error("HTTPError %s", err)
			time.sleep(3)
			request = urllib.request.Request(url, headers={ 'User-Agent': 'Wget/1.9.1' })  # User-Agent hack for getting
			response = urlopen(request)
			logging.debug("Received response %.10s", response)
		return response
