from main import Main


#  benchmark.pedantic(something, setup=my_special_setup, args=(1, 2, 3), kwargs={'foo': 'bar'}, iterations=10,rounds = 100)

def test_foo ():
	parser = Main(7)
	benchmark.pedantic(Main.run, args=parser, iterations=2, rounds=10)


test_foo()
