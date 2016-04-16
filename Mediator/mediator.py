import sys
import threading
from queue import Queue

from base_class import BaseClass


class Mediator(BaseClass):
	def __init__ (self, seed: list, input_size: int):
		super().__init__()

		self._input_size = input_size
		self._urls_get = 0
		self._items_parsed = 0
		self._responses_set = 0

		self._url_qlock = threading.Lock()
		self._url_queue = Queue()

		self._model_qlock = threading.Lock()
		self._model_queue = Queue()

		self._response_qlock = threading.Lock()
		self._response_queue = Queue()

		for item in seed:
			self._url_queue.put(item)

	def get_url (self, count=1):
		if count < 1:
			raise AttributeError
		else:
			urls = None
			try:
				self._url_qlock.acquire()  # TODO: use await for better thread utilization
				if not self._url_queue.empty():
					urls = self._url_queue.get(count)  # TODO: get n{1-5, or benchmarks} urls (for await statement)
					self._urls_get += count
			finally:
				self._url_qlock.release()
			return urls

	def push_urls (self, urls: list):
		try:
			self._url_qlock.acquire()  # TODO: use await for better thread utilization
			if not self._url_queue.empty():
				for url in urls:
					self._url_queue.put(url)
		finally:
			self._url_qlock.release()

	def get_models (self):
		raise NotImplementedError

	# TODO: Derivative type Model
	def push_models (self, models: list):
		self._items_parsed += len(models)
		raise NotImplementedError

	def get_response (self, count=1):
		raise NotImplementedError

	# TODO: Response class
	def push_response (self, response):
		self._responses_set += 1
		raise NotImplementedError

	def update_progressbar (self):
		"""
		Updates progress bar when thread ended a task
		"""
		if self._url_queue.qsize() > 0:
			count_progress = int((1 - (self._url_queue.qsize() / self._input_size)) * 100)
		else:
			count_progress = 100
		progress_bar = ""
		for i in range(0, 20):
			if i < int(count_progress / 5):
				progress_bar += "|"
			else:
				progress_bar += " "
		sys.stdout.write("\r")
		sys.stdout.write("%s %s Urls get: %d, Responses set: %d, Items parsed: %d" % (
			progress_bar, str(count_progress), self._urls_get, self._responses_set, self._items_parsed))
		sys.stdout.flush()

	def keep_workers (self):
		return not (self._url_queue.empty() and self._model_queue.empty() and self._response_queue.empty())

	def keep_crawler (self):
		return not self._url_queue.empty()

	def keep_parser (self):
		return not self._response_queue.empty()

	def keep_database (self):
		return not self._model_queue.empty()
