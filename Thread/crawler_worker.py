from Thread.base_worker import BaseWorker


class CrawlerWorker(BaseWorker):
	def task (self):
		raise NotImplementedError
