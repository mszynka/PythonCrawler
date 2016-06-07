from Base.base_class import BaseClass
from Base.base_iterable import BaseIterable


class Response(BaseClass):
	def __init__ (self, url: str, html: str):
		super().__init__()
		self.html = html
		self.url = url


class Responses(BaseIterable):
	def clear (self):
		self._objects.clear()
