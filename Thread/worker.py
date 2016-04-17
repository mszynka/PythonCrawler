import threading

from Base.base_class import BaseClass
from Crawl.crawler import Crawler
from Database.models import Models
from Mediator.mediator import Mediator
from Parse.parser import Parser
from Thread.crawler_worker import CrawlerWorker
from Thread.database_worker import DatabaseWorker
from Thread.parser_worker import ParserWorker


class Worker(BaseClass, threading.Thread):
	def __init__ (self, mediator: Mediator, max_workers: int):
		"""
		Default constructor
		:type mediator: Mediator Design Pattern
		:type max_workers: Max workers
		"""
		super().__init__()
		threading.Thread.__init__(self)
		self.mediator = mediator
		self.logger.debug("Initialized. Assuming %3d max threads", max_workers)

		# Define workers
		self.parse_worker = ParserWorker(self.mediator)
		self.crawl_worker = CrawlerWorker(self.mediator)
		self.database_worker = DatabaseWorker(self.mediator)
		self.parser = Parser()

	def run (self) -> None:
		"""
		Default overriden thread run method
		"""
		keep_worker = True
		self.mediator.update_progressbar()

		while keep_worker:
			# Get data
			in_urls = self.mediator.get_url()
			out_urls = list()
			models = Models()

			# Parse
			if in_urls is not None:
				for url in in_urls:
					omodel, ourl = self.parse_and_log_time(url)
					out_urls.append(ourl)
					models.append(omodel)

				# Save
				self.mediator.push_urls(out_urls)
				self.mediator.push_models(models)

				self.mediator.update_progressbar()
			keep_worker = self.mediator.keep_workers()

	# TODO: change to mediator and workers
	def parse_and_log_time (self, url: str) -> tuple:
		"""
		Runs webcrawler, logger and timer for self.logger.and statistics
		:param url: URL as entry point for webcrawler
		:returns: Parsed data from webcrawler
		"""
		self.logger.debug("Acquired some data and starts processing")

		response = Crawler().execute_request(url)
		if response:
			data_model, urls = self.parser.parse(response)
		else:
			data_model = None
			urls = list()

		return data_model, urls
