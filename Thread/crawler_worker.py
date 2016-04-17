from Crawl.crawler import Crawler
from Parse.response import Responses
from Thread.base_worker import BaseWorker


class CrawlerWorker(BaseWorker):
	def task (self):
		# Init
		self.mediator.update_progressbar()
		in_urls = self.mediator.get_url()
		responses = Responses()

		# Crawl
		if in_urls is not None:
			for url in in_urls:
				responses.append(Crawler().execute_request(url))

		# Save
		self.mediator.push_responses(responses)

		# Return
		return self.mediator.keep_crawler()
