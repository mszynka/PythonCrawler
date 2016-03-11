from Thread.thread import ThreadParser


class ThreadManager:
	def __init__ (self, max_workers):
		self.max_workers = max_workers
		self._threads = []
		self.threads_data = []

	def create_threads (self):
		for i in range(1, self.max_workers + 1):
			self._threads.append(ThreadParser(i, self.max_workers + 1))

	def start_threads (self):
		for thread in self._threads:
			thread.start()

	def join_and_collect_data (self):
		for thread in self._threads:
			thread.join()
			self.threads_data.extend(thread.parsed_data_array)

	def process_on_all_workers (self):
		self.create_threads()
		self.start_threads()
		self.join_and_collect_data()
