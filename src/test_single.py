from sqlalchemy.orm import scoped_session
from db import queries, session_factory


session = scoped_session(session_factory)()

for query in queries:
    result = session.execute(query)
    print(list(result)[0])
    print(result.rowcount)

session.close()
