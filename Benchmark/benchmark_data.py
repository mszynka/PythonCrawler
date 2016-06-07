import os

from Base.base_class import BaseClass
from Base.singleton import Singleton
from Benchmark.benchmark_status import BenchmarkStatus


@Singleton
class BenchmarkData(BaseClass):
	def __init__ (self):
		super().__init__()
		self.data = dict()

	def appendd (self, moduleName, method, time):
		status = BenchmarkStatus.Instance()
		# print(moduleName)
		try:
			if os.environ["BENCHMARK"]:
				if not self.data[moduleName]:
					self.data[moduleName] = list()
				iteration, round = status.get()
				self.data[moduleName].appendd({ method: (time, iteration, round) })
		except KeyError:
			self.logger.debug("Not a benchmark run.")

	def print (self):
		print(self.data)
