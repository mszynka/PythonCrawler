import sys
import threading
from timeit import default_timer as timer

from Crawl.crawler import Crawler
from Parse.parser import Parser
from base_class import BaseClass


class ThreadParser(BaseClass, threading.Thread):
	def __init__ (self, manager):
		"""
		Default constructor
		:param manager: To access parent thread
		"""
		super().__init__()
		threading.Thread.__init__(self)
		self.manager = manager
		self.logger.debug("Thread initialized. Assuming %3d max threads", self.manager.max_workers)
		self.parser = Parser()

	def run (self):
		"""
		Default overriden thread run method
		"""
		self.logger.debug("Thread running")
		exit_flag = False

		while not exit_flag:
			# Lock
			self.manager.qlock.acquire()  # TODO: use await for better thread utilization
			if not self.manager.queue.empty():
				url = self.manager.queue.get()  # TODO: get n{1-5, or benchmarks} urls (for await statement)
				self.manager.qlock.release()

				# Parse
				parsed_data = self.parse_and_log_time(url)
				self.update_progressbar()

				# Return
				self.return_data_to_manager(parsed_data)
			else:  # Exiting thread if queue is empty
				self.manager.qlock.release()
				exit_flag = True

		self.logger.debug("Thread finished")

	def parse_and_log_time (self, url: str):
		"""
		Runs parser, logger and timer for self.logger.and statistics
		:param url: URL as entry point for parser
		:returns: Parsed data from parser
		"""
		self.logger.debug("Thread acquired some data and starts processing")

		start = timer()
		response = Crawler().execute_request(url)
		if response:
			parsed_data = self.parser.parse(response, url)
		else:
			parsed_data = None
		end = timer()

		self.logger.debug("Thread finished processing. Elapsed: %.2f s", end - start)
		return parsed_data

	# TODO: Model class
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
		progress_bar = ""
		for i in range(0, 20):
			if i < int(count_progress / 5):
				progress_bar += "|"
			else:
				progress_bar += " "
		sys.stdout.write("\r")
		sys.stdout.write(
			progress_bar + " " + str(count_progress) + "% Time elapsed: " + format(timer() - self.manager.start_time,
			                                                                       ".2f") + "s")
		sys.stdout.flush()
