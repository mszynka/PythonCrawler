import cProfile

from main import Main

webcrawler = Main(max_threads=2)
cProfile.run(webcrawler.run())
