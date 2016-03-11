import time
import urllib
from urllib.error import HTTPError
from urllib.request import urlopen

from bs4 import BeautifulSoup
from pyquery import PyQuery

from Database import model


def parser (list_of_urls, pid, array_len):
	parser_data = []

	for url in list_of_urls:
		print(format((list_of_urls.index(url)/len(list_of_urls))*100, '3.0f') + "%\tThread " + format(
				pid, '3d') + ", " + url)

		try:
			request = urllib.request.Request(url, headers={ 'User-Agent': 'Wget/1.9.1' })  # User-Agent hack for getting
			response = urlopen(request)
		except HTTPError:
			time.sleep(3)
			request = urllib.request.Request(url, headers={ 'User-Agent': 'Wget/1.9.1' })  # User-Agent hack for getting
			response = urlopen(request)
		encoding = response.info().get_charset()
		soup_string = BeautifulSoup(response.read(), 'html.parser')
		if encoding is not None and soup_string.original_encoding != encoding:
			soup_string = BeautifulSoup(response, from_encoding=encoding)

		pq_parsed = PyQuery(soup_string.decode())
		site_main = pq_parsed('div.site-main')
		content = site_main('.entry-content')

		pheader = site_main('.entry-header')
		pbody = content('pre:first')
		pchords = content('p + pre')

		p = model.ParsedObject(header=pheader.text(), body=pbody.text(), chords=pchords.text(), url=url)
		parser_data.append(p)

	return parser_data
