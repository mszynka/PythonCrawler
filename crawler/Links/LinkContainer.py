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
