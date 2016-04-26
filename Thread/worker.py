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
		keep_worker = True
		self.mediator.update_progressbar()
		self.crawl_worker.start()
		self.parse_worker.start()
		self.database_worker.start()

		while keep_worker:
			self.crawl_worker.join(3)  # TODO: Benchmark perfect time
			self.parse_worker.join(3)
			self.database_worker.join(3)
			keep_worker = self.crawl_worker.is_alive() and self.parse_worker.is_alive() and self.database_worker.is_alive()
