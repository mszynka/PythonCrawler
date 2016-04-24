import sys

import input
from Base.base_class import BaseClass
from Mediator.mediator import Mediator
from Thread.worker import Worker


class WorkerManager(BaseClass):
	def __init__ (self, max_workers: int):
		"""
		Default constructor
		Intializing threads list, queues with locks
		:param max_workers: Max number of threads used as workers
		"""
		super().__init__()
		self._max_workers = max_workers
		self._threads = list()
		self._input_size = len(input.links_list)
		self.mediator = Mediator(input.links_list, self._input_size)
		self.logger.debug("Initialized with %d elements in queue", len(input.links_list))

	def create_threads (self):
		"""
		Creates workers
		"""
		for i in range(0, self._max_workers):
			self._threads.append(Worker(self.mediator, self._max_workers))
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
		self.logger.debug("Started processing on all workers with %d elements in queue", self._input_size)
		self.create_threads()
		self.start_threads()
		self.join_all()

		# Dirtyfix for avoiding \r in thread
		sys.stdout.write("\n")
