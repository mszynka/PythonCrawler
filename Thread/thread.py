import threading

import input
from Parse.parser import parser


class ThreadParser(threading.Thread):
	def __init__ (self, thread_id, max_thread_number):
		threading.Thread.__init__(self)
		self.thread_id = thread_id
		self.max_thread_number = max_thread_number
		self.parsed_data_array = []

	def run (self):
		partition = len(input.links_list) / self.max_thread_number
		index = int(partition * self.thread_id)
		tmp_max_index = int((self.thread_id + 1) * partition)
		max_index = tmp_max_index
		if tmp_max_index > len(input.links_list):
			max_index = len(input.links_list)

		self.parsed_data_array = parser(input.links_list[index:max_index], self.thread_id, len(input.links_list))
