from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Database import model


class DatabaseManager:
	def __init__ (self):
		self.engine = create_engine('sqlite:///Database/parsed.db')
		model.Base.metadata.create_all(self.engine)
		self.session = sessionmaker(bind=self.engine)()

	def add (self, data):
		self.session.add(data)
		self.session.commit()

	def add_many (self, data):
		for data in data:
			self.session.add(data)

		self.session.commit()

	def list (self):
		pass
