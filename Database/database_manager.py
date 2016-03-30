import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Database import model


class DatabaseManager:
	def __init__ (self):
		"""
		Default constructor
		Setting up Database Engine, paths, binding models and creating session
		"""
		db_path = "sqlite:///Database/parsed.db"
		self.engine = create_engine(db_path)
		model.Base.metadata.create_all(self.engine)
		self.session = sessionmaker(bind=self.engine)()
		self.logger = logging.getLogger(type(self).__name__)
		self.logger.debug("DatabaseManager: Session started with path: %s", db_path)

	def add (self, data):
		"""
		Adds an data object to session
		:param data: Model type data object
		"""
		try:
			self.session.add(data)
			self.session.commit()
			self.logger.debug("Element %s added", data.header)
		except AttributeError as err:
			self.logger.error("AtributeError: %s", err)

	def add_many (self, data):
		"""
		Adds many from list
		:param data: Model type data list
		"""
		try:
			for data in data:
				self.session.add(data)

			self.session.commit()
			self.logger.debug("%d elements added", len(data))
		except ValueError as err:
			self.logger.error("Value error: %s", err)

	def add_queue (self, queue):
		"""
		Adds many from queue
		:param queue: Model type data queue
		"""
		while not queue.empty():
			element = queue.get()
			# Checking if element is not none to ensure that there is provided data
			if element is not None:
				self.add(element)

	def list (self):
		"""
		Prints out whole database as list
		"""
		raise NotImplementedError
