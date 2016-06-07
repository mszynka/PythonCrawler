from Crawl.crawler import Crawler
from Parse.response import Responses
from Thread.base_worker import BaseWorker


class CrawlerWorker(BaseWorker):
	def task (self) -> bool:
		# Init
		self.mediator.update_progressbar()
		url = self.mediator.get_url()
		responses = Responses()
		responses.clear()

		# Crawl
		if url is not None:
			self.logger.debug("Got %d urls", len(url))
			responses_tmp = Crawler().execute_request(url)
			responses.append(responses_tmp)
			self.logger.debug("Executed %s", url)

			# Save
			self.mediator.push_responses(responses)
			if len(responses) > 0:
				self.logger.info("Pushed %d responses", len(responses))

		# Return
		return self.mediator.keep_crawler()
