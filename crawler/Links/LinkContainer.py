from urllib.parse import urlparse

from crawler.Links.LinkContainerException import LinkContainerException
from debugTools import Debug


class LinkContainer:
	def __init__ (self, dictionary=None):
		"""
		Constructor
		:param dictionary: Dict element as init param
		"""
		self.dict = dictionary
		self.linksCrawledOverCounter = 0
		self.linksToCrawlCounter = 0

	def __add__ (self, element):
		"""
		Insert's element into container
		:param element: Element to insert
		:raises LinkContainerException
		"""
		if not isinstance(element, dict) or not isinstance(element, []) or not isinstance(element, str):
			raise LinkContainerException(
				"LinkContainer.add's param element is not valid instance of a dictionary, an array or string", element)

		# TODO: implement
		raise NotImplementedError()

	def __bool__ (self):
		"""
		True if all links are already crawled over
		:return boolean
		:raises LinkContainerException
		"""
		return self.linksCrawledOverCounter == self.linksToCrawlCounter

	def __getitem__ (self):
		"""
		Returns last item that hadn't been crawled over
		:return string
		:raises LinkContainerException
		"""
		# TODO: increment/decrement suitable properties
		# TODO: change returned element flag
		pass

	def __contains__ (self, item):
		"""
		# Boolean upon item existence
		:param item: Item name as dict key
		:return boolean
		:raises LinkContainerException
		"""
		# TODO: Attention! Is synchronous. May consume time!
		pass

	def __delitem__ (self, key):
		"""
		Deletes item with given key
		:param key: Dict key
		:raises LinkContainerException
		"""
		# TODO: Attention! Is synchronous. May consume time!
		pass

	def __str__ (self):
		"""
		Returns elements
		:return string
		:raises LinkContainerException
		"""
		# TODO: Attention! Is synchronous. May consume time!
		pass

	def __setitem__ (self, key, value):
		"""
		Inserts element's value for given key
		:param key: Element's key
		:param value: Element's value
		:raises LinkContainerException
		"""
		pass

	def add (self, element):
		""" [Public method]
		Insert's element into container
		:param element: Element to insert
		:raises LinkContainerException
		"""
		try:
			self.__add__(element)
		except LinkContainerException as e:
			print(e)
		except Exception as e:
			raise LinkContainerException(None, self, e)

	def get_next_item (self):
		""" [Public method]
		Returns next item to crawl over
		:raises LinkContainerException
		"""
		try:
			self.__getitem__()
		except LinkContainerException as e:
			print(e)
		except Exception as e:
			raise LinkContainerException(None, self, e)

	@property
	def has_next_item (self):
		""" [Public property]
		Returns true if there are items to crawl over
		:return: boolean
		:raises LinkContainerException
		"""
		try:
			return not self.__bool__()
		except LinkContainerException as e:
			print(e)
		except Exception as e:
			raise LinkContainerException(None, self, e)


def tokenize_links (links):
	"""
	Link tokenizer for smart management
	:param links: Links array or string
	:return: Parsed links dict
	"""
	outputLinksDict = dict()

	if isinstance(links, list):
		Debug.log("LinkAnalyzer found list of links", Debug.Severity.DebugInfo)
		for link in links:
			tmp_url = urlparse(link)
			if tmp_url.path != '':
				if tmp_url.netloc in outputLinksDict:
					outputLinksDict[tmp_url.netloc].append({ tmp_url.path: False })
				else:
					outputLinksDict[tmp_url.netloc] = [{ tmp_url.path: False }]
			else:
				outputLinksDict[tmp_url.netloc] = [{ "/": False }]
		return outputLinksDict
	elif isinstance(links, str):
		Debug.log("LinkAnalyzer found single link", Debug.Severity.DebugInfo)
		tmp_url = urlparse(links)
		if tmp_url.path != '':
			outputLinksDict[tmp_url.netloc] = [{ tmp_url.path: False }]
		else:
			outputLinksDict[tmp_url.netloc] = [{ "/": False }]
		return outputLinksDict
