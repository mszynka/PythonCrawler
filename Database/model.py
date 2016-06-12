from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Concepts(Base):
	'''
	Database SqlAlchemy model for simple data to SQLite binding.
	This is top level container model.
	ConceptId is an UUID generated string to bind data from CData.
	ConceptName is a name of the container.
	'''
	__tablename__ = 'Concepts'

	Id = Column(Integer, primary_key=True)
	ConceptId = Column(String)
	ConceptName = Column(String)


class CData(Base):
	'''
	Database SqlAlchemy model for simple data to SQLite binding.
	This is key-value child of Concepts table.
	ConceptId is duplicate from parent to bind data after database commit.
	Key is name of the property and Value is a value for given key.
	'''
	__tablename__ = 'CData'

	Id = Column(Integer, primary_key=True)
	ConceptId = Column(String)
	Key = Column(String)
	Value = Column(String)
