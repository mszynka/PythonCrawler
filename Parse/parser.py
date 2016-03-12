import logging
import time
import urllib
from urllib.error import HTTPError
from urllib.request import urlopen

from bs4 import BeautifulSoup
from pyquery import PyQuery

from Database import model


def execute_request (url, pid):
	"""
	Executes a request on given URL
	:param url: URL to get the response
	:param pid: Process ID for logging purposes
	:returns: urllb.request.urlopen response
	"""
	try:
		request = urllib.request.Request(url, headers={ 'User-Agent': 'Wget/1.9.1' })  # User-Agent hack for getting
		response = urlopen(request)
		logging.debug("Parser on thread %d: received response %.10s", pid, response)
	except HTTPError as err:
		logging.error("HTTPError %s", err)
		time.sleep(3)
		request = urllib.request.Request(url, headers={ 'User-Agent': 'Wget/1.9.1' })  # User-Agent hack for getting
		response = urlopen(request)
		logging.debug("Parser on thread %d: received response %.10s", pid, response)
	return response


def parse_response (response, url, pid):
	"""
	Parses response from urlopen
	:param response: urrlib.request.urlopen product
	:param url: URL for logging purposes
	:param pid: Process ID for logging purposes
	:returns: Model
	"""
	encoding = response.info().get_charset()
	soup_string = BeautifulSoup(response.read(), 'html.parser')
	if encoding is not None and soup_string.original_encoding != encoding:
		soup_string = BeautifulSoup(response, from_encoding=encoding)
		logging.debug("Parser on thread %d: encoding mismatch. Parsed with %s", pid, encoding)

	# Invent another parsing method
	logging.debug("Parser on thread %d: Initialized parsing with PyQuery", pid)
	pq_parsed = PyQuery(soup_string.decode())
	site_main = pq_parsed('div.site-main')
	content = site_main('.entry-content')
	pheader = site_main('.entry-header')
	pbody = content('pre:first')
	pchords = content('p + pre')

	p = model.ParsedObject(header=pheader.text(), body=pbody.text(), chords=pchords.text(), url=url)
	logging.debug("Parser on thread %d: Parsing successful", pid)
	return p


def parser (url, pid):
	"""
	Entry function for parsing HTTP requests
	:param url: URL to request
	:param pid: Process ID for multithreading (in case of single thread put 0 or whatever)
	:returns: Model
	"""
	logging.debug("Parser: %s", url)

	response = execute_request(url, pid)
	if response:
		return parse_response(response, url, pid)
	else:
		return None
