import logging
import sys
import threading
from timeit import default_timer as timer

from Parse.parser import parser


class ThreadParser(threading.Thread):
	def __init__ (self, thread_id, manager):
		"""
		Default constructor
		:param thread_id: If multithreading sets Thread ID for logging and identibility purposes
		:param manager: To access parent thread
		"""
		threading.Thread.__init__(self)
		self.manager = manager
		self.thread_id = thread_id
		logging.debug("Thread %3d initialized. Assuming %3d max threads", thread_id, self.manager.max_workers)

	def run (self):
		"""
		Default overriden thread run method
		"""
		logging.debug("Thread %3d running", self.thread_id)
		exit_flag = False

		while not exit_flag:
			# Lock
			self.manager.qlock.acquire()  # TODO: use await for better thread utilization
			if not self.manager.queue.empty():
				url = self.manager.queue.get()
				self.manager.qlock.release()
				# Parse
				parsed_data = self.parse_and_log_time(url)
				self.update_progressbar()
				# Return
				self.return_data_to_manager(parsed_data)
			else:  # Exiting thread if queue is empty
				self.manager.qlock.release()
				exit_flag = True

		logging.debug("Thread %3d finished", self.thread_id)

	def parse_and_log_time (self, url):
		"""
		Runs parser, logger and timer for logging and statistics
		:param url: URL as entry point for parser
		:returns: Parsed data from parser
		"""
		logging.debug("Thread %3d acquired some data and starts processing", self.thread_id)
		start = timer()
		parsed_data = parser(url, self.thread_id)
		end = timer()
		logging.debug("Thread %3d finished processing. Elapsed: %.2f s", self.thread_id, end - start)
		return parsed_data

	def return_data_to_manager (self, parsed_data):
		"""
		Writes parsed data to output queue
		:param parsed_data: Parsed data from parser
		"""
		self.manager.out_qlock.acquire()
		self.manager.out_queue.put(parsed_data)
		self.manager.out_qlock.release()

	def update_progressbar (self):
		"""
		Updates progress bar when thread ended a task
		"""
		if self.manager.queue.qsize() > 0:
			count_progress = int((1 - (self.manager.queue.qsize() / self.manager.input_size)) * 100)
		else:
			count_progress = 100
		sys.stdout.write("\r")
		# TODO: redo formating this section
		sys.stdout.write(
			"Progress: " + str(count_progress) + "% Time elapsed: " + format(timer() - self.manager.start_time,
			                                                                 ".2f") + "s")
		sys.stdout.flush()
