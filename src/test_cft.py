from concurrent.futures import ThreadPoolExecutor, as_completed
from sqlalchemy.orm import scoped_session
from db import queries, session_factory, engine


def execute_query(query):
    session = scoped_session(session_factory)()
    result = session.execute(query)
    session.close()
    return result

with ThreadPoolExecutor(max_workers=engine.pool.size()) as executor:
    futures = [executor.submit(execute_query, query) for query in queries]

    for future in as_completed(futures):
        result = future.result()
        print(list(result)[0])
        print(result.rowcount)

