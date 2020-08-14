from sqlalchemy.orm import scoped_session
from threading import Thread
from db import queries, session_factory


def execute_query(query):
    session = scoped_session(session_factory)()
    result = session.execute(query)
    print(list(result)[0])
    print(result.rowcount)
    session.close()


for query in queries:
    Thread(target=execute_query, args=(query,)).start()
