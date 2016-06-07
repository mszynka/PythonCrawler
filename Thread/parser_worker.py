from Database.model import ParsedObject
from Database.models import Models
from Mediator.mediator import Mediator
from Parse.parser import Parser
from Parse.response import Response
from Thread.base_worker import BaseWorker


class ParserWorker(BaseWorker):
	def __init__ (self, mediator: Mediator, parent, parser: Parser):
		super().__init__(mediator, parent)
		self.parser = parser

	def task (self) -> bool:
		# Init
		self.mediator.update_progressbar()
		responses = self.mediator.get_responses()
		models = Models()
		urls = list()

		# Parse
		if responses is not None:
			self.logger.debug("Got %d responses", len(responses))
			for response in responses:
				if response is not None and isinstance(response, Response):
					model, url = self.parser.parse(response)
					if model is not None and isinstance(model, ParsedObject):
						models.append(model)
					if urls is not None:
						urls.append(url)
					self.logger.debug("Parsed %s", response.url)

			# Save
			self.mediator.push_models(models)
			self.mediator.push_urls(urls)
			if len(models) > 0:
				self.logger.info("Pushed %d models", len(models))
			if len(urls) > 0:
				self.logger.info("Pushed %d urls", len(urls))

		# Return
		return self.mediator.keep_parser() or self.mediator.keep_crawler()