import threading
from queue import Queue

from base_class import BaseClass


class Mediator(BaseClass):
	def __init__ (self):
		super().__init__()

		self._url_qlock = threading.Lock()
		self._url_queue = Queue()

		self._model_qlock = threading.Lock()
		self._model_queue = Queue()

		self._response_qlock = threading.Lock()
		self._response_queue = Queue()

	def get_url (self, count=1):
		raise NotImplementedError

	def push_urls (self, urls: list):
		raise NotImplementedError

	def _send_models (self):
		raise NotImplementedError

	# TODO: Derivative type Model
	def push_models (self, model):
		raise NotImplementedError

	def get_response (self, count=1):
		raise NotImplementedError

	def push_response (self, response):
		raise NotImplementedError
