import os
from unittest import TestCase

from sqlalchemy.orm import class_mapper

from Database.database_manager import DatabaseManager
from Database.model import Concepts
from Tests.Mocks import Mock


class TestDatabaseManager(TestCase):
	def setUp (self):
		self.dbpath = "/Tests/Database/test.sqlite"
		self.dbmanager = DatabaseManager("sqlite://" + self.dbpath)

	def tearDown (self):
		os.remove(os.getcwd() + self.dbpath)

	def test_add (self):
		model = Mock.model()

		self.dbmanager.add(model)
		model_get = self.dbmanager.session.query(class_mapper(model.__class__)).all()[0]

		self.assertEqual(model.ConceptId, model_get.ConceptId)

	def test_add_many (self):
		counter = 0
		max = 15

		for i in range(5, max):
			with self.subTest(i=i):
				models = Mock.models(i)
				counter += i

				self.dbmanager.add_many(models)
				count = len(self.dbmanager.session.query(class_mapper(models.first().__class__)).all())

				self.assertEqual(counter, count)

	def test_add_queue (self):
		counter = 0
		max = 15

		for i in range(5, max):
			with self.subTest(i=i):
				models_queue = Mock.models_queue(i)
				counter += i

				self.dbmanager.add_queue(models_queue)
				# FIX: dynamically get class name
				count = len(self.dbmanager.session.query(class_mapper(Concepts)).all())

				self.assertEqual(counter, count)

	def test_list (self):
		model = Mock.model()
		self.dbmanager.add(model)

		lst = self.dbmanager.list(model)

		self.assertEqual(lst[0], model)
