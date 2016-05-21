import sys
from io import StringIO

from Benchmark.benchmark_status import BenchmarkStatus
from Benchmark.datagrid import datagrid
from Benchmark.time_capsule import time_capsule


class Benchmark:
	def __init__ (self):
		self._data_grids = list()
		self._stdouts = list()
		self._stderrs = list()

	def progress (self, iteration, round, hasErrors=False):
		count_progress = int(((iteration + 1) * 10 + round + 1) / (self.iterations * 10 + self.rounds) * 100)
		progress_bar = ""
		for i in range(0, 20):
			if i < int(count_progress / 5):
				progress_bar += "|"
			else:
				progress_bar += " "
		sys.stdout.write("\r")
		sys.stdout.write("[%s %s%%] Iter: %i Round: %i" % (progress_bar, str(count_progress), iteration + 1, round + 1))
		sys.stdout.flush()

	# noinspection PyUnboundLocalVariable
	def stats (self, callback, iterations, rounds, output=False):
		self.iterations = iterations
		self.rounds = rounds
		status = BenchmarkStatus.Instance()

		for i in range(0, iterations):
			for r in range(0, rounds):
				status.set(i, r)
				capsule = time_capsule()
				capsule.start()

				if not output:
					capture = StringIO()
					capture_err = StringIO()
					save_stderr = sys.stderr
					save_stdout = sys.stdout
					sys.stdout = capture
					sys.stderr = capture_err

				callback(i).run()

				if not output:
					sys.stdout = save_stdout
					sys.stderr = save_stderr
					self._stdouts.append(capture.getvalue())
					self._stderrs.append(capture_err.getvalue())

				capsule.end()
				self._data_grids.append(datagrid(i, r, capsule.get_time()))
				if not output:
					self.progress(i, r, len(self._stderrs[len(self._stderrs) - 1]) > 0)

		print()
		datagrid.print_collection(datagrid.avg_by_iteration(self._data_grids))
		# BenchmarkData.Instance().print()
		self._logErrors()
		return self

	def _logErrors (self):
		if len(self._stderrs) > 0:
			f = open("benchmark_err.log", "w")
			f.writelines(self._stderrs)
