from urllib.parse import urlparse

from debugTools import Debug


class LinkAnalyzer:
	@staticmethod
	def tokenize_links (links):
		"""
		Link tokenizer for smart management
		:param links: Links array or string
		:return: Parsed links array
		"""
		outputLinks = dict()

		if isinstance(links, list):
			Debug.log("LinkAnalyzer found list of links", Debug.Severity.DebugInfo)
			for link in links:
				tmp_url = urlparse(link)
				if tmp_url.path != '':
					if tmp_url.netloc in outputLinks:
						outputLinks[tmp_url.netloc].append(tmp_url.path)
					else:
						outputLinks[tmp_url.netloc] = [tmp_url.path]
				else:
					outputLinks[tmp_url.netloc] = ["/"]
			return outputLinks
		elif isinstance(links, str):
			Debug.log("LinkAnalyzer found single link", Debug.Severity.DebugInfo)
			tmp_url = urlparse(links)
			if tmp_url.path != '':
				outputLinks[tmp_url.netloc] = [tmp_url.path]
			else:
				outputLinks[tmp_url.netloc] = ["/"]
			return outputLinks
