import re
import time
import urllib
import uuid
from queue import Queue
from urllib.error import HTTPError
from urllib.request import urlopen
from xml.dom import minidom

from Database.model import Concepts
from Database.models import Models
from Parse.response import Response, Responses


class Mock:
	# TODO: Toggle when random urls implemented
	hasSingleUrl = True

	@staticmethod
	def url ():
		# TODO: return different url at random from specified format
		return "http://spiewnikreligijny.pl"

	@staticmethod
	def urls (count=2):
		urls = list()

		for i in range(0, count):
			urls.append(Mock.url())

		return urls

	# FIX: Do uniqueness module
	@staticmethod
	def urls_unique (count=2):
		urls = list()

		for i in range(0, count):
			urls.append(Mock.url())

		return urls

	@staticmethod
	def model ():
		# TODO: return different models at random (denote type as param)
		return Concepts(ConceptId=Mock.model_id(), ConceptName=Mock.model_name())

	@staticmethod
	def models (count=2):
		models = Models()

		for i in range(0, count):
			models.append(Mock.model())

		return models

	@staticmethod
	def model_id ():
		return str(uuid.uuid4())

	@staticmethod
	def model_name ():
		# TODO: return different names at random
		return "Sample concept name"

	@staticmethod
	def models_queue (count):
		queue = Queue()

		models = Mock.models(count)
		for model in models:
			queue.put(model)

		return queue

	@staticmethod
	def response (url=None):
		global request
		if not url:
			url = Mock.url()
		try:
			request = urllib.request.Request(url, headers={ 'User-Agent': 'Wget/1.9.1' })
		except HTTPError as err:
			time.sleep(3)
			request = urllib.request.Request(url, headers={ 'User-Agent': 'Wget/1.9.1' })
		finally:
			return Response(url, urlopen(request))

	@staticmethod
	def responses (count=2):
		responses = Responses()

		for i in range(0, count):
			responses.append(Mock.response())

		return responses

	@staticmethod
	def template (url):
		url_dict = dict()
		xmldoc = minidom.parse("Parse/Templates/spiewnik.xml")
		for site in xmldoc.getElementsByTagName('site'):
			listamoja = []
			for concept in site.getElementsByTagName('concept'):
				li = [{ obj.attributes['name'].value: obj.attributes['query'].value } for obj in
				      concept.getElementsByTagName('object')]
				la = { concept.attributes['name'].value: li }
				listamoja.extend([la])
			url_dict[site.attributes['url'].value] = listamoja

		for a in sorted(url_dict, reverse=True):
			if re.match(r'^' + a + '(\D*\d*\D*\d*)*$', url):
				return url_dict[a]
