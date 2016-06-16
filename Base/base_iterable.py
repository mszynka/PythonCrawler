from abc import ABCMeta

from Base.base_class import BaseClass


class BaseIterable(BaseClass, metaclass=ABCMeta):
	def __init__ (self, objects=None):
		super().__init__()
		if objects is None:
			self._objects = list()
		else:
			assert isinstance(objects, list)
			self._objects = objects

	def append (self, obj) -> None:
		if obj is not None:
			self._objects.append(obj)

	def extend (self, obj) -> None:
		if obj is not None and isinstance(obj, list):
			self._objects.extend(obj)

	def first (self):
		if len(self._objects):
			return self._objects[0]
		return None

	def __len__ (self) -> int:
		return len(self._objects)

	def __iter__ (self):
		for obj in self._objects:
			yield obj

	def clear (self):
		self._objects.clear()
