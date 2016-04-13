from Thread.base_worker import BaseWorker


class DatabaseWorker(BaseWorker):
	def task (self):
		raise NotImplementedError
