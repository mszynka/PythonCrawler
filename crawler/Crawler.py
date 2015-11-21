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
		pass


# TODO: implement crawling methods (leave analytics to analytics module)
def test_crawler (url, word, maxPages):
	"""
		Crawler temporary test function
		:param url: base url to start crawling with
		:param word: string you're searching for on urls
		:param maxPages: maximum pages to crawl (link order defines the sequence)
	"""
	pagesToVisit = LinkAnalyzer.tokenize_links(url)  # Crawler page's links array
	numberVisited = 0  # Number of already visited links
	numberFoundWords = 0  # Number of found matching words during crawling
	parser = LinkParser() # Parser initialization

	while numberVisited < maxPages and pagesToVisit != []:
		numberVisited += 1
		url = pagesToVisit[0].geturl()
		pagesToVisit = pagesToVisit[1:]
		try:
			Debug.log(str.join(" ", [numberVisited.__str__(), " Visiting: ", url]), Debug.Severity.DebugInfo)
			data, links = parser.get_links(url)
			if data.find(word) > -1:
				numberFoundWords += 1
				Debug.log(" **Success!**", Debug.Severity.Info)
			pagesToVisit += links
		except urllib.error.HTTPError as e:
			Debug.log(str.join(" ", [str(e.code), str(e.reason)]), Debug.Severity.Warning)
			return e.code
		except:
			Debug.log(str.join(" ", [" **Failed!** ", str(sys.exc_info()[0])]), Debug.Severity.Warning)

	if numberFoundWords > 0:
		Debug.log(str.join(" ", ["The word", word, "was found at", url,
						 numberFoundWords.__str__(),
								 "times"]),
				  Debug.Severity.Info)
		return True
	else:
		Debug.log("Word never found", Debug.Severity.Info)
		return False
