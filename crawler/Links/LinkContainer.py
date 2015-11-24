from urllib.parse import urlparse

from debugTools import Debug


class LinkContainer:
	def __init__ (self, dictionary=None):
		"""
		Constructor
		:param dictionary: Dict element as init param
		"""
		self.dict = dictionary

	def __add__ (self, element):
		"""
		Insert's element into container
		:param element: Element to insert
		:raises LinkContainerException
		"""
		pass

	def __bool__ (self):
		"""
		True if all links are already crawled over
		:return boolean
		"""
		pass

	def __getitem__ (self):
		"""
		Returns last item that hadn't been crawled over
		:return string
		"""
		pass

	def __contains__ (self, item):
		"""
		# Boolean upon item existence
		:param item: Item name as dict key
		:return boolean
		"""
		pass

	def __delitem__ (self, key):
		"""
		Deletes item with given key
		:param key: Dict key
		:raises LinkContainerException
		"""
		pass

	def __str__ (self):
		"""
		Returns elements
		:return string
		"""
		pass

	def __setitem__ (self, key, value):
		"""
		Inserts element's value for given key
		:param key: Element's key
		:param value: Element's value
		:raises LinkContainerException
		"""
		pass


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
