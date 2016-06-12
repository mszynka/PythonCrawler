import uuid

from pyquery import PyQuery

from Base.base_class import BaseClass
from Database.model import Concepts, CData
from Database.models import Models


class TemplateParser(BaseClass):
	def parse (self, html, template):
		pq_parser = PyQuery(html)
		lista = Models()

		for con in template:
			ConName = [x for x in con][0]
			ConId = uuid.uuid4().__str__()
			newConcept = Concepts(ConceptName=ConName, ConceptId=ConId)
			lista.extend(
				[CData(ConceptId=ConId, Key=[i for i in v][0], Value=(pq_parser([v[i] for i in v][0]).html())) for v in
				 [con[x] for x in con][0]])
			lista.append(newConcept)
		return lista
