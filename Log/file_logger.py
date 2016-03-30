import logging

from Log.base_logger import BaseLogger


class FileLogger(BaseLogger):
	def __init__ (self, max_threads):
		super().__init__()
		self._max_threads = max_threads

	def configure (self):
		"""
		Configures logger and initiates logging by inserting info message
		"""
		logging.basicConfig(filename="parser.log", level=logging.DEBUG, filemode='w',
		                    format='%(asctime)s %(thread)d:%(module)-15s %(name)-12s %(levelname)-8s %(message)s',
		                    datefmt='%m-%d %H:%M')
		logging.info("Started with max threads: %d", self._max_threads)
