from Base.singleton import Singleton


@Singleton
class BenchmarkStatus:
	def __init__ (self):
		self.iteration_count = 0
		self.round_count = 0

	def get (self):
		return self.iteration_count, self.round_count

	def set (self, iter, round):
		self.iteration_count = iter
		self.round_count = round
