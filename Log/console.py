import logging

from Log.base import BaseLogger


class ConsoleLogger(BaseLogger):
	def configure (self):
		"""
		Defines custom console logger for development and info for user
		"""
		console_level = logging.WARNING  # Change level for console logger in development mode
		console_formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

		logging.basicConfig(format=console_formatter, level=console_level)
