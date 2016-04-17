from abc import ABCMeta

from Base.base_class import BaseClass


class BaseIterable(BaseClass, metaclass=ABCMeta):
	def __init__ (self, objects=list()):
		super().__init__()
		assert isinstance(objects, list)
		self._objects = objects

	def append (self, obj) -> None:
		self._objects.append(obj)

	def __len__ (self) -> int:
		return len(self._objects)

	def __iter__ (self):
		for obj in self._objects:
			yield obj
