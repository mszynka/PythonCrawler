import uuid

from pyquery import PyQuery

from Base.base_class import BaseClass
from Database.model import Concepts, CData

__author__ = 'robin'


class TemplateParser(BaseClass):
	def parse (self, html, template):
		pq_parser = PyQuery(html)

		for con in template:
			ConName = [x for x in con][0]
			ConId = uuid.uuid4()
			newConcept = Concepts(ConceptName=ConName, ConceptId=ConId)
			lista = [CData(ConceptId=ConId, Key=[i for i in v][0], Value=pq_parser([v[i] for i in v][0])) for v in
			         [con[x] for x in con][0]]
			lista.append(newConcept)
			return lista
