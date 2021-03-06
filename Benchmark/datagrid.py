from Benchmark.benchmark_status import BenchmarkStatus


class datagrid:
	def __init__ (self, iteration, round, time):
		self.iteration = iteration
		self.round = round
		self.time = time

	def __repr__ (self):
		return str("%i\t%.2f" % (self.iteration + 1, self.time))

	@staticmethod
	def avg_by_iteration (collection):
		out = list()

		for item in collection:
			if len(out) > 0:
				if out[len(out) - 1].iteration == item.iteration:
					out[len(out) - 1].round += 1
					out[len(out) - 1].time += item.time
				else:
					out.append(item)
			else:
				out.append(item)

		for item in out:
			item.time = float(item.time / (item.round + 1))

		return out

	@staticmethod
	def print_collection (collection):
		f = open('benchmark.log', 'a')
		f.write("=============================================\n")
		i, r = BenchmarkStatus.Instance().get()
		f.write(str.format("Iterations: {0}, rounds: {1}\n", i + 1, r + 1))
		for item in collection:
			print(item)
			f.write(str(item))
			f.write("\n")
