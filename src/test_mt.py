import string
from os import environ
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from threading import Thread

USER = environ["DATABASE_USER"]
PASSWORD = environ["DATABASE_PASSWORD"]
DATABASE = "employees"

engine = create_engine("mysql+pymysql://{}:{}@localhost/{}".format(USER, PASSWORD, DATABASE))
session_factory = sessionmaker(bind=engine)

raw_query = """
SELECT employees.first_name, employees.last_name, dept_manager.emp_no, departments.dept_name FROM employees
    INNER JOIN dept_emp ON dept_emp.emp_no = employees.emp_no
    INNER JOIN dept_manager ON dept_manager.dept_no = dept_emp.dept_no
    INNER JOIN departments ON departments.dept_no = dept_emp.dept_no
    WHERE employees.first_name LIKE '{}%'
    ORDER BY first_name
    LIMIT 5000
"""

queries = list(map(lambda char: raw_query.format(char), string.ascii_uppercase))

results = []


def execute_query(query):
    session = scoped_session(session_factory)()
    result = session.execute(query)
    results.append(result)
    print(len(results))


for query in queries:
    Thread(target=execute_query, args=(query,)).start()