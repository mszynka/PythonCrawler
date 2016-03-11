import threading

import input
from parser import parser


class ParserThread(threading.Thread):
	def __init__ (self, thread_id, max_thread_number):
		threading.Thread.__init__(self)
		self.threadID = thread_id
		self.maxThreadNumber = max_thread_number
		self.parsed_data_array = []

	def run (self):
		partition = len(input.links_list) / self.maxThreadNumber
		index = int(partition * self.threadID)
		tmp_max_index = int((self.threadID + 1) * partition)
		max_index = tmp_max_index
		if tmp_max_index > len(input.links_list):
			max_index = len(input.links_list)

		self.parsed_data_array = parser(input.links_list[index:max_index], self.threadID, len(input.links_list))
