from concurrent.futures import ProcessPoolExecutor
from sqlalchemy.orm import scoped_session
from db import queries, session_factory


def execute_query(query):
    session = scoped_session(session_factory)()
    result = session.execute(query)
    session.close()
    return result


with ProcessPoolExecutor(max_workers=2) as executor:
    for result in executor.map(execute_query, queries):
        print(list(result)[0])
        print(result.rowcount)

