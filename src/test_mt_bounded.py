from sqlalchemy.orm import scoped_session
from threading import Thread, BoundedSemaphore
from db import queries, session_factory, engine

pool_semaphore = BoundedSemaphore(value=engine.pool.size())


def execute_query(query):
    with pool_semaphore:
        session = scoped_session(session_factory)()
        result = session.execute(query)
        session.close()
        print(list(result)[0])
        print(result.rowcount)


for query in queries:
    Thread(target=execute_query, args=(query,)).start()

