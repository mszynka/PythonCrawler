from Database.database_manager import DatabaseManager
from Mediator.mediator import Mediator
from Thread.base_worker import BaseWorker


class DatabaseWorker(BaseWorker):
	def __init__ (self, mediator: Mediator, parent, db: DatabaseManager):
		super().__init__(mediator, parent)
		self.db = db

	def task (self) -> bool:
		# Init
		models = self.mediator.get_models()

		# Save
		if len(models) > 0 and models is not None:
			self.db.add_many(models)
			self.logger.info("Saved %d tuples", len(models))

		# Return
		return self.mediator.keep_database()
