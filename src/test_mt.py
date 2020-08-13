from sqlalchemy.orm import scoped_session
from threading import Thread
from db import queries, session_factory


def execute_query(query):
    session = scoped_session(session_factory)()
    result = session.execute(query)
    print(result[0])
    print(result.rowcount)


for query in queries:
    Thread(target=execute_query, args=(query,)).start()
