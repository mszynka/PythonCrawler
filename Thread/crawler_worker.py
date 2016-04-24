from Crawl.crawler import Crawler
from Parse.response import Responses
from Thread.base_worker import BaseWorker


class CrawlerWorker(BaseWorker):
	def task (self) -> bool:
		# Init
		self.mediator.update_progressbar()
		in_urls = self.mediator.get_url()
		responses = Responses()

		# Crawl
		if in_urls is not None:
			self.logger.debug("Got %d urls", len(in_urls))
			for url in in_urls:
				responses.append(Crawler().execute_request(url))
				self.logger.debug("Executed %s", url)

		# Save
		self.mediator.push_responses(responses)
		self.logger.debug("Pushed %d responses", len(responses))

		# Return
		return self.mediator.keep_crawler()
