"""
----------------------
	 Main module
----------------------
"""
from timeit import default_timer as timer

from Base.base_class import BaseClass
from Log.logger_manager import LoggerManager
from Thread.worker_manager import WorkerManager


class Main(BaseClass):
	def __init__ (self, max_threads: int):
		"""
		Default constructor
		Initiates DB mediator, Thread mediator and max workers
		:param max_threads: Max workers value
		"""
		super().__init__()
		self.max_threads = max_threads
		self.tmanager = WorkerManager(max_threads)
		self.logmanager = LoggerManager()

	def run (self):
		self.logmanager.config_loggers()
		self.logger.info("Started with max threads: %d", self.max_threads)

		start = timer()
		self.tmanager.process_on_all_workers(start)
		end = timer()

		self.logger.info("Finished. Elapsed time: %.2f", end - start)
