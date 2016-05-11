import threading

from Base.base_class import BaseClass
from Database.database_manager import DatabaseManager
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
		self.parser = Parser()
		self.db = DatabaseManager()

		self.parse_worker = ParserWorker(self.mediator, self, self.parser)
		self.crawl_worker = CrawlerWorker(self.mediator, self)
		self.database_worker = DatabaseWorker(self.mediator, self, self.db)

	def run (self) -> None:
		"""
		Default overriden thread run method
		"""
		keep_crawler = True
		keep_parser = True
		keep_db = True
		self.mediator.update_progressbar()

		while keep_crawler and keep_parser and keep_db:
			keep_crawler = self.crawl_worker.run()
			keep_parser = self.parse_worker.run()
			keep_db = self.database_worker.run()
