"""
----------------------
	Crawler module
----------------------
"""
import time
import urllib
from urllib.error import HTTPError
from urllib.request import urlopen

from Base.base_class import BaseClass
from Benchmark.benchmark_data import BenchmarkData
from Benchmark.time_capsule import time_capsule
from Parse.response import Response


class Crawler(BaseClass):
	def _get_response (self, url) -> Response:
		# User-Agent hack for getting requests out of sites not supporting robots
		request = urllib.request.Request(url, headers={ 'User-Agent': 'Wget/1.9.1' })
		self.logger.debug("Received response")
		return Response(url, urlopen(request))

	def execute_request (self, url: str) -> Response:
		"""
		Executes a request on given URL
		:param url: URL to get the response
		:returns: urllb.request.urlopen response
		"""
		if url is None:
			return False
		response = None
		capsule = time_capsule()
		capsule.start()

		try:
			response = self._get_response(url)
		except HTTPError as err:
			self.logger.error("HTTPError %s", err)
			time.sleep(3)
			response = self._get_response(url)
		finally:
			capsule.end()
			data = BenchmarkData.Instance()
			data.appendd(type(self).__name__, self.execute_request.__name__, capsule.get_time())
			return response