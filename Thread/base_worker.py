import threading
from abc import abstractmethod
from timeit import default_timer as timer

from Base.base_class import BaseClass
from Mediator.mediator import Mediator


class BaseWorker(BaseClass, threading.Thread):
	def __init__ (self, mediator: Mediator, parent):
		super().__init__()
		threading.Thread.__init__(self)
		self._parent = parent
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
	def task (self) -> bool:
		pass
