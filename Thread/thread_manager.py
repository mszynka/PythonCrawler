import sys
import threading
from queue import Queue

import input
from Thread.thread import ThreadParser
from base_class import BaseClass


class ThreadManager(BaseClass):
	def __init__ (self, max_workers):
		"""
		Default constructor
		Intializing threads list, queues with locks
		:param max_workers: Max number of threads used as workers
		"""
		super().__init__()
		self.max_workers = max_workers
		self._threads = []
		self.input_size = len(input.links_list)
		# Input queue with lock
		self.qlock = threading.Lock()
		self.queue = Queue()
		# Output queue with lock
		self.out_qlock = threading.Lock()
		self.out_queue = Queue()
		# Initializing input queue
		for item in input.links_list:
			self.queue.put(item)
		# TODO: create self.logger with format interceptor with class name or throw it into global interceptor
		self.logger.debug("Initialized with %d elements in queue", len(input.links_list))

	def create_threads (self):
		"""
		Creates workers
		"""
		for i in range(0, self.max_workers):
			self._threads.append(ThreadParser(self))
		self.logger.debug("Created %d threads", len(self._threads))

	def start_threads (self):
		"""
		Starts workers
		"""
		for thread in self._threads:
			thread.start()
		self.logger.debug("Started all %d threads", len(self._threads))

	def join_all (self):
		"""
		Waits for threads to terminate
		"""
		# TODO: use await for better thread utilization
		for thread in self._threads:
			thread.join()
		self.logger.debug("Joined all %d threads", len(self._threads))

	def process_on_all_workers (self, start=None):
		"""
		Creates workers, adds jobs and runs them for computing. Then returns results by threads (output queue)
		:param start: Master thread start time
		"""
		# noinspection PyAttributeOutsideInit
		self.start_time = start
		self.logger.debug("Started processing on all workers with %d elements in queue", self.queue.qsize())
		self.create_threads()
		self.start_threads()
		self.join_all()

		# Dirtyfix for avoiding \r in thread
		sys.stdout.write("\n")
