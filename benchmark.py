from Benchmark.benchmark import benchmark
from main import Main

b = benchmark()
b.stats(Main, iterations=10, rounds=10)

# http://matplotlib.org
# TODO: implement benchmarking tool
