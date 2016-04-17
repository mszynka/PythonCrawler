import logging

from Log.base import BaseLogger


class FileLogger(BaseLogger):
	def __init__ (self):
		super().__init__()
		self.filename = 'webcrawler.log'

	def configure (self):
		"""
		Configures logger and initiates logging by inserting info message
		"""
		logging.basicConfig(filename=self.filename, level=logging.DEBUG, filemode='a',
		                    format='%(asctime)s %(threadName)-12s %(name)-17s %(levelname)-8s %(message)s',
		                    datefmt='%m-%d %H:%M:%S')

		with open(self.filename, "a") as log:
			log.write("========================================================================================\n")
