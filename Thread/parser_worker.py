from Thread.base_worker import BaseWorker


class ParserWorker(BaseWorker):
	def task (self):
		raise NotImplementedError
