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

from Parse.links import LinkParser


class Crawler(Thread):
	def __init__ (self):
		super().__init__()
		self._parser = LinkParser()  # Parser initialization
		self._pagesVisited = list()  # List of already visited links
		self._pagesToVisit = dict()  # Dict of pages to crawl
		self.logger = logging.getLogger(type(self).__name__)

	def crawl (self, url):
		"""
				Crawler crawling method
				:param url: base url to start crawling with
				:return: boolean upon success/failure
			"""
		self._pagesToVisit = self._parser.tokenize_links(url)  # Crawler page's links array

		url = "http://" + str(list(self._pagesToVisit.keys())[0])
		self.logger.info("Crawling: " + url)
		self._pagesVisited.append(url)
		# self._pagesToVisit = self._pagesToVisit[1:]
		# noinspection PyBroadException
		try:
			self.logger.debug(str.join(" ", [len(self._pagesVisited), " Visiting: ", url]))
			data, links = self._parser.get_links(url)
			self._pagesToVisit += links
		except urllib.error.HTTPError as e:
			self.logger.debug(str.join(" ", [str(e.code), str(e.reason)]))
			return e.code
		except:
			self.logger.error(sys.exc_info())
			return False

		self.logger.info(str.join(" ", ["Visited", str(len(self._pagesVisited)), "pages"]))
		return True

	def execute_request (self, url):
		"""
		Executes a request on given URL
		:param url: URL to get the response
		:returns: urllb.request.urlopen response
		"""
		try:
			request = urllib.request.Request(url, headers={ 'User-Agent': 'Wget/1.9.1' })  # User-Agent hack for getting
			response = urlopen(request)
			self.logger.debug("Received response %.10s", response)
		except HTTPError as err:
			self.logger.error("HTTPError %s", err)
			time.sleep(3)
			request = urllib.request.Request(url, headers={ 'User-Agent': 'Wget/1.9.1' })  # User-Agent hack for getting
			response = urlopen(request)
			self.logger.debug("Received response %.10s", response)
		return response
