import logging

from Log.base_logger import BaseLogger


class ConsoleLogger(BaseLogger):
	def configure (self):
		"""
		Defines custom console logger for development and info for user
		"""
		console = logging.StreamHandler()
		console.setLevel(logging.WARNING)  # Change level for console logger in development mode
		formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
		console.setFormatter(formatter)
		logging.getLogger('').addHandler(console)
