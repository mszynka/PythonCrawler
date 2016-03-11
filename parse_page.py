from timeit import default_timer as timer

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import model
from thread import ParserThread

engine = create_engine('sqlite:///parsed.db')
model.Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()

threads = []
maxThreadsNumber = 7

for i in range(1, maxThreadsNumber + 1):
	threads.append(ParserThread(i, maxThreadsNumber + 1))

start = timer()
for thread in threads:
	thread.start()

parsed_data = []

for thread in threads:
	thread.join()
	parsed_data.extend(thread.parsed_data_array)

end = timer()
print("Elapsed time: ", end - start)

for data in parsed_data:
	session.add(data)

session.commit()
