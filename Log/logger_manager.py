from Log.console_logger import ConsoleLogger
from Log.file_logger import FileLogger


class LoggerManager:
	def __init__ (self, max_threads):
		self._max_threads = max_threads

	def config_loggers (self):
		"""
		Configures all required loggers
		"""
		FileLogger(self._max_threads).configure()
		ConsoleLogger().configure()
