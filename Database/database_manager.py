from queue import Queue

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import UnmappedInstanceError

from Base.base_class import BaseClass
from Database import model
from Database.model import Base
from Database.models import Models


class DatabaseManager(BaseClass):
	def __init__ (self):
		"""
		Default constructor
		Setting up Database Engine, paths, binding models and creating session
		"""
		super().__init__()
		db_path = "sqlite:///Database/data.sqlite"
		self.engine = create_engine(db_path)
		model.Base.metadata.create_all(self.engine)
		self.session = sessionmaker(bind=self.engine)()
		self.logger.debug("DatabaseManager: Session started with path: %s", db_path)

	def add (self, data: Base):
		"""
		Adds an data object to session
		:param data: Model type data object
		"""
		assert isinstance(data, Base)
		try:
			if data is not None:
				self.session.add(data)
				self.session.commit()
				self.logger.debug("Element %s added", data.header)
		except AttributeError as err:
			self.logger.error("AtributeError: %s", err)
		except AssertionError as err:
			self.logger.error("AssertionError: %s", err)
		except UnmappedInstanceError as err:
			self.logger.error("UnmappedInstanceError: %s", err)

	def add_many (self, data_container: list):
		"""
		Adds many from list
		:param data_container: Model type data list
		"""
		assert isinstance(data_container, Models)
		try:
			for data in data_container:
				if isinstance(data, Base):
					self.session.add(data)

			self.session.commit()
			self.logger.debug("%d elements added", len(data_container))
		except ValueError as err:
			self.logger.error("Value error: %s", err)

	def add_queue (self, queue: Queue):
		"""
		Adds many from queue
		:param queue: Model type data queue
		"""
		assert isinstance(queue, Queue)
		while not queue.empty():
			element = queue.get()
			assert isinstance(element, Base)
			# Checking if element is not none to ensure that there is provided data
			if element is not None:
				self.add(element)

	def list (self):
		"""
		Prints out whole database as list
		"""
		raise NotImplementedError
