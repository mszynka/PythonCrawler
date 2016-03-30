"""
----------------------
	 Main module
----------------------
"""
import logging
from timeit import default_timer as timer

from Database.database_manager import DatabaseManager
from Thread.thread_manager import ThreadManager


class Main:
	def __init__ (self, max_threads):
		"""
		Default constructor
		Initiates DB manager, Thread manager and max workers
		:param max_threads: Max workers value
		"""
		self.dbmanager = DatabaseManager()
		self.max_threads = max_threads
		self.tmanager = ThreadManager(max_threads)

	def configure_file_logger (self):
		"""
		Configures logger and initiates logging by inserting info message
		"""
		logging.basicConfig(filename="parser.log", level=logging.DEBUG, filemode='w',
		                    format='%(asctime)s %(thread)d:%(module)-15s %(name)-12s %(levelname)-8s %(message)s',
		                    datefmt='%m-%d %H:%M')
		logging.info("Started with max threads: %d", self.max_threads)

	@staticmethod
	def configure_console_logger ():
		"""
		Defines custom console logger for development and info for user
		"""
		console = logging.StreamHandler()
		console.setLevel(logging.WARNING)  # Change level for console logger in development mode
		formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
		console.setFormatter(formatter)
		logging.getLogger('').addHandler(console)

	def compute_with_tmanager (self):
		"""
		Start Thread manager processing
		"""
		start = timer()
		self.tmanager.process_on_all_workers(start)
		end = timer()
		logging.info("Thread manager finished working. Elapsed time: %.2f", end - start)

	def run (self):
		self.configure_file_logger()
		self.configure_console_logger()
		self.compute_with_tmanager()
		self.dbmanager.add_queue(self.tmanager.out_queue)

		logging.info("Finished parsing")
