from timeit import default_timer as timer

from Database.database_manager import DatabaseManager
from Thread.thread_manager import ThreadManager

tmanager = ThreadManager(7)
start = timer()
tmanager.process_on_all_workers()
end = timer()
print("Elapsed time: ", end - start)

dbmanager = DatabaseManager()
dbmanager.add_many(tmanager.threads_data)
