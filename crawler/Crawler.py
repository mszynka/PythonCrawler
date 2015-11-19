"""
-------------------
	Web crawler
-------------------
	Credits: http://www.netinstructions.com/how-to-make-a-web-crawler-in-under-50-lines-of-python-code/
"""

import sys
from threading import Thread
from urllib3.exceptions import HTTPError
from crawler.LinkParser import LinkParser
from debugTools import Debug


class Crawler:
	class CrawlerWorker(Thread):
		pass


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
			Debug.log(str.join(" ", [numberVisited.__str__(), " Visiting: ", url]), Debug.Severity.DebugInfo)
			parser = LinkParser()
			data, links = parser.get_links(url)
			if data.find(word) > -1:
				numberFoundWords += 1
				pagesToVisit += links
				Debug.log(" **Success!**", Debug.Severity.Info)
		except HTTPError as e:
			Debug.log(str.join(" ", [e.code, e.reason]), Debug.Severity.Warning)
			return e.code
		except:
			Debug.log(str.join(" ", [" **Failed!** ", sys.exc_info()[0]].__str__), Debug.Severity.Warning)

	if numberFoundWords > 0:
		Debug.log(str.join(" ", ["The word", word, "was found at", url, numberFoundWords.__str__(), "times"]),
		          Debug.Severity.Info)
		return True
	else:
		Debug.log("Word never found", Debug.Severity.Info)
		return False
