import os

from Benchmark.benchmark import Benchmark
from main import Main

os.environ["BENCHMARK"] = "True"

b = Benchmark()
b.stats(Main, iterations=10, rounds=10, output=False)

# http://matplotlib.org
# TODO: implement benchmarking tool
