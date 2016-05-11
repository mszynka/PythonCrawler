from pytest_benchmark.plugin import benchmark

from main import Main


def test_foo ():
	webcrawler = Main(7)
	benchmark.pedantic(webcrawler.run, iterations=10, rounds=10)


test_foo()

# http://matplotlib.org
# TODO: implement benchmarking tool
