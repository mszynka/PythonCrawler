import sys
import threading
from queue import Queue

from Base.base_class import BaseClass
from Database.models import Models
from Parse.response import Response, Responses


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

	def get_url (self, count=1) -> list:
		assert (count > 0)
		urls = None
		try:
			self._url_qlock.acquire()  # TODO: use await for better thread utilization
			if not self._url_queue.empty():
				urls = self._url_queue.get()  # TODO: count  # TODO: get n{1-5, or benchmarks} urls (for await
				#  statement)
				self._urls_get += count
		finally:
			self._url_qlock.release()
		return urls

	def push_urls (self, urls: list) -> None:
		try:
			self._url_qlock.acquire()  # TODO: use await for better thread utilization
			if not self._url_queue.empty():
				for url in urls:
					self._url_queue.put(url)
		finally:
			self._url_qlock.release()

	def get_models (self) -> Models:
		models = Models()
		try:
			self._model_qlock.acquire()  # TODO: use await for better thread utilization
			while not self._model_queue.empty():
				models.append(self._model_queue.get())
		finally:
			self._model_qlock.release()
		return models

	def push_models (self, models: Models) -> None:
		assert isinstance(models, Models)
		try:
			self._model_qlock.acquire()  # TODO: use await for better thread utilization
			self._items_parsed += 1
			if not self._model_queue.empty():
				for model in models:
					self._model_queue.put(model)
		finally:
			self._model_qlock.release()

	def get_responses (self, count=1) -> Responses:
		assert (count > 0)
		responses = Responses()
		try:
			self._response_qlock.acquire()  # TODO: use await for better thread utilization
			if not self._response_queue.empty():
				responses.append(
					self._response_queue.get())  # TODO: count  # TODO: get n{1-5, or benchmarks} urls (for await
			# statement)
		finally:
			self._response_qlock.release()
		return responses

	# TODO: Assertion tests with usages, types and magic
	def push_response (self, response: Response) -> None:
		if isinstance(response, Response) and response is not None:
			try:
				self._response_qlock.acquire()  # TODO: use await for better thread utilization
				self._response_queue.put(response)
				self._responses_set += 1
			finally:
				self._response_qlock.release()

	def push_responses (self, responses: Responses) -> None:
		if isinstance(responses, Responses) and responses is not None:
			try:
				self._response_qlock.acquire()  # TODO: use await for better thread utilization
				for response in responses:
					if response is not None:
						self._response_queue.put(response)
						self._responses_set += 1
			finally:
				self._response_qlock.release()

	def update_progressbar (self):
		"""
		Updates progress bar when thread ended a task
		"""
		if self._url_queue.qsize() > 0:
			count_progress = int((1 - (self._urls_get / self._url_queue.qsize())) * 100)
		else:
			count_progress = 100
		progress_bar = ""
		for i in range(0, 20):
			if i < int(count_progress / 5):
				progress_bar += "|"
			else:
				progress_bar += " "
		sys.stdout.write("\r")
		sys.stdout.write("%s %s%% Urls set: %d, Urls get: %d, Responses set: %d, Items parsed: %d" % (
			progress_bar, str(count_progress), self._url_queue.__sizeof__(), self._urls_get, self._responses_set,
			self._items_parsed))
		sys.stdout.flush()

	def keep_workers (self) -> bool:
		return not (self.keep_crawler() and self.keep_parser() and self.keep_database())

	def keep_crawler (self) -> bool:
		return self.keep_parser()

	# return not self._url_queue.empty()

	def keep_parser (self) -> bool:
		return not (self._url_queue.__sizeof__() <= self._items_parsed)

	def keep_database (self) -> bool:
		return not (self._urls_get >= self._items_parsed)

	# return not self._model_queue.empty()
