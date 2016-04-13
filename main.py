"""
----------------------
	 Main module
----------------------
"""
from timeit import default_timer as timer

from Database.database_manager import DatabaseManager
from Log.logger_manager import LoggerManager
from Thread.thread_manager import ThreadManager
from base_class import BaseClass


class Main(BaseClass):
	def __init__ (self, max_threads: int):
		"""
		Default constructor
		Initiates DB manager, Thread manager and max workers
		:param max_threads: Max workers value
		"""
		super().__init__();
		self.dbmanager = DatabaseManager()
		self.max_threads = max_threads
		self.tmanager = ThreadManager(max_threads)
		self.logmanager = LoggerManager()

	def compute_with_tmanager (self):
		"""
		Start Thread manager processing
		"""
		start = timer()
		self.tmanager.process_on_all_workers(start)
		end = timer()
		self.logger.info("Thread manager finished working. Elapsed time: %.2f", end - start)

	def run (self):
		self.logmanager.config_loggers()
		self.logger.info("Started with max threads: %d", self.max_threads)
		self.compute_with_tmanager()
		self.dbmanager.add_queue(self.tmanager.out_queue)

		self.logger.info("Finished parsing")
