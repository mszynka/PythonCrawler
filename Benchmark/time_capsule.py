from time import time


class time_capsule:
	def __init__ (self):
		self._time_start = 0
		self._time_end = 0

	def start (self):
		self._time_start = self.current_milli_time()
		return self

	def end (self):
		self._time_end = self.current_milli_time()
		return self

	def get_time (self):
		return int(self._time_end - self._time_start)

	@staticmethod
	def current_milli_time ():
		return int(round(time() * 1000))
