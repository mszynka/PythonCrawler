from unittest import TestCase

from analytics.LinkAnalyzer import LinkAnalyzer


class TestLinkAnalyzer(TestCase):
	def test_tokenize_links_dictionary (self):
		self.assertIsInstance(LinkAnalyzer.tokenize_links("http://thewebsite.com"), dict)

	def test_tokenize_links_dictionary_single_value (self):
		base_url = "http://thewebsite.com"
		for i in ["/", "/index", "/index.html", "/app/running/test", "/another%link%type"]:
			link = "".join([base_url, i])
			with self.subTest():
				self.assertDictEqual(LinkAnalyzer.tokenize_links(link), { base_url.split("//")[1]: [i] })

	def test_tokenize_links_dictionary_multiple_values (self):
		base_url = "http://thewebsite.com"
		links = []
		list_container = []
		for i in ["/", "/index", "/index.html", "/app/running/test", "/another%link%type"]:
			links.append("".join([base_url, i]))
			list_container.append(i)
			with self.subTest():
				self.assertDictEqual(LinkAnalyzer.tokenize_links(links), { base_url.split("//")[1]: list_container })
