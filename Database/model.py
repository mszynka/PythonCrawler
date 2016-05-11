from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ParsedObject(Base):
	__tablename__ = 'ptext'

	id = Column(Integer, primary_key=True)
	header = Column(Unicode)
	body = Column(Unicode)
	url = Column(Unicode)
