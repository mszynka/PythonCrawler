"""
----------------------
	Parser module
----------------------
"""
import logging

from bs4 import BeautifulSoup
from pyquery import PyQuery

from Crawl.crawler import Crawler
from Database import model

logger = logging.getLogger("Parser")


def parse_response (response, url):
	"""
	Parses response from urlopen
	:param response: urrlib.request.urlopen product
	:param url: URL for logger.purposes
	:returns: Model
	"""
	encoding = response.info().get_charset()
	soup_string = BeautifulSoup(response.read(), 'html.parser')
	if encoding is not None and soup_string.original_encoding != encoding:
		soup_string = BeautifulSoup(response, from_encoding=encoding)
		logger.debug("Encoding mismatch. Parsed with %s", encoding)

	# TODO: Invent another parsing method
	logger.debug("Initialized parsing with PyQuery")
	try:
		pq_parsed = PyQuery(soup_string.decode())
		site_main = pq_parsed('div.site-main')
		content = site_main('.entry-content')
		pheader = site_main('.entry-header')
		pbody = content('pre:first')
		pchords = content('p + pre')

		p = model.ParsedObject(header=pheader.text(), body=pbody.text(), chords=pchords.text(), url=url)
		logger.debug("Parsing successful")
		return p
	except:
		logger.error("Parsing was unsuccessful")


def parser (url):
	"""
	Entry function for parsing HTTP requests
	:param url: URL to request
	:returns: Model
	"""
	logger.debug("Starting with url: %s", url)

	response = Crawler().execute_request(url)
	if response:
		return parse_response(response, url)
	else:
		return None
