from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Concepts(Base):
	__tablename__ = 'Concepts'

	Id = Column(Integer, primary_key=True)
	ConceptId = Column(String)
	ConceptName = Column(String)


class CData(Base):
	__tablename__ = 'CData'

	Id = Column(Integer, primary_key=True)
	ConceptId = Column(String)
	Key = Column(String)
	Value = Column(String)
