import threading
from abc import abstractmethod
from timeit import default_timer as timer

from Mediator.mediator import Mediator
from base_class import BaseClass


class BaseWorker(BaseClass, threading.Thread):
	def __init__ (self, mediator: Mediator):
		super().__init__()
		self.mediator = mediator

	def run (self):
		self.logger.debug("Running")
		keep_worker = True
		while keep_worker:
			start = timer()
			keep_worker = self.task()
			end = timer()
			self.logger.debug("Finished processing. Elapsed: %.2f s", end - start)

		self.logger.debug("Worker finished")

	@abstractmethod
	def task (self):
		pass
