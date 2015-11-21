from urllib.parse import urlparse


class LinkAnalyzer:
	@staticmethod
	def tokenize_links(links):
		outputLinks = []

		if type(links) == type([]):
			for link in links:
				outputLinks.append(urlparse(link))
		else:
			outputLinks = [urlparse(links)]

		outputLinks = sorted(outputLinks, key=lambda link: link.netloc)

		return outputLinks
