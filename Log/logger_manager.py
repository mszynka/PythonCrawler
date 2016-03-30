from Log.console import ConsoleLogger
from Log.file import FileLogger


# noinspection PyMethodMayBeStatic
class LoggerManager:
	def config_loggers (self):
		"""
		Configures all required loggers
		"""
		FileLogger().configure()
		ConsoleLogger().configure()
