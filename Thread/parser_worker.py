from Database.model import ParsedObject
from Database.models import Models
from Mediator.mediator import Mediator
from Parse.parser import Parser
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
				model, url = self.parser.parse(response)
				if model is not None and isinstance(model, ParsedObject):
					models.append(model)
				if urls is not None:
					urls.append(url)
				self.logger.debug("Parsed %s", response.url)

			# Save
			self.mediator.push_models(models)
			self.mediator.push_urls(urls)
			self.logger.debug("Pushed %d models", len(models))
			self.logger.debug("Pushed %d urls", len(urls))

		# Return
		return self.mediator.keep_parser() or self._parent.crawl_worker.is_alive()
