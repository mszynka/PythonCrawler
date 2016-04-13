import threading

from Crawl.crawler import Crawler
from Mediator.mediator import Mediator
from Parse.parser import Parser
from Thread.crawler_worker import CrawlerWorker
from Thread.database_worker import DatabaseWorker
from Thread.parser_worker import ParserWorker
from base_class import BaseClass


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

	def run (self):
		"""
		Default overriden thread run method
		"""
		self.logger.debug("Running")
		keep_worker = True

		while keep_worker:
			# Get data
			url = self.mediator.get_url()

			# Parse
			data_model, urls = self.parse_and_log_time(url)

			# Save
			self.mediator.push_urls(urls)
			self.mediator.push_models(data_model)

			self.mediator.update_progressbar()
			keep_worker = self.mediator.keep_workers()

		self.logger.debug("Worker finished")

	# TODO: change to mediator and add threads for parsing, crawling and analytics
	def parse_and_log_time (self, url: str):
		"""
		Runs parser, logger and timer for self.logger.and statistics
		:param url: URL as entry point for parser
		:returns: Parsed data from parser
		"""
		self.logger.debug("Acquired some data and starts processing")

		response = Crawler().execute_request(url)
		if response:
			data_model, urls = self.parser.parse(response, url)
		else:
			data_model = None
			urls = list()

		return data_model, urls
