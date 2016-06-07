import sys
import threading
from queue import Queue

from Base.base_class import BaseClass
from Database.model import ParsedObject
from Database.models import Models
from Parse.response import Response, Responses


class Mediator(BaseClass):
	def __init__ (self, seed: list, input_size: int):
		super().__init__()

		self._input_size = input_size
		self._urls_get = 0
		self._items_parsed = 0
		self._responses_set = 0
		self._urls_set = input_size

		self._url_qlock = threading.Lock()
		self._urls = dict()

		self._model_qlock = threading.Lock()
		self._model_queue = Queue()

		self._response_qlock = threading.Lock()
		self._response_queue = Queue()

		for item in seed:
			self._urls[item] = False

	def get_url (self, count=1) -> list:
		if len(self._urls) < 1:
			return None

		assert (count > 0)
		urls = list()

		tmp_count = count
		for item in self._urls:
			if not self._urls[item]:
				self._urls[item] = True
				tmp_count -= 1
				urls.append(item)

			if tmp_count < 1:
				break

		if len(urls):
			self._urls_get += count
			urls = urls[0] if count == 1 else urls
			return urls
		return None

	def push_urls (self, urls: list) -> None:
		if self._urls_set >= 100:
			return

		for url in urls:
			try:
				self._urls[url]
			except KeyError:
				self._urls[url] = False
				self._urls_set += 1

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
			if not self._model_queue.empty():
				for model in models:
					if isinstance(model, ParsedObject):
						self._model_queue.put(model)
						self._items_parsed += 1
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
		if len(self._urls) > 0:
			count_progress = int((self._urls_get / self._urls_set) * 100)
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
			progress_bar, str(count_progress), self._urls_set, self._urls_get, self._responses_set,
			self._items_parsed))
		sys.stdout.flush()

	def keep_workers (self) -> bool:
		return not (self.keep_crawler() and self.keep_parser() and self.keep_database())

	def keep_crawler (self) -> bool:
		# return self._urls.unfinished_tasks > 0
		if self._urls_get > 50:
			return not self._urls_get >= self._urls_set
		else:
			return not self._urls_get > self._urls_set

	def keep_parser (self) -> bool:
		# return self._urls.qsize() > self._items_parsed
		return self.keep_crawler()  # For a while this may be working

	def keep_database (self) -> bool:
		# return self.keep_crawler() and (self._model_queue.qsize() > 0)
		return self.keep_crawler()  # For a while this may be working

	# return not self._model_queue.empty()
