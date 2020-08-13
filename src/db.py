import string

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import environ
from sqlalchemy import text

raw_query = """
SELECT CONCAT(reports.first_name, ' ', reports.last_name) AS employee_name, average_salary, CONCAT(managers.first_name, ' ', managers.last_name) AS manager_name, departments.dept_name FROM employees reports
    INNER JOIN dept_emp ON dept_emp.emp_no = reports.emp_no
    INNER JOIN dept_manager ON dept_manager.dept_no = dept_emp.dept_no
    INNER JOIN employees managers ON managers.emp_no = dept_manager.emp_no
    INNER JOIN departments ON departments.dept_no = dept_emp.dept_no
    INNER JOIN (
        SELECT FLOOR(AVG(salaries.salary)) as average_salary, salaries.emp_no FROM salaries
        GROUP BY salaries.emp_no
    ) AS average_salaries ON average_salaries.emp_no = reports.emp_no
    WHERE reports.first_name LIKE '{}%'
    ORDER BY reports.first_name
    LIMIT 5000
"""

queries = list(map(lambda char: raw_query.format(char), string.ascii_uppercase))

USER = environ["DATABASE_USER"]
PASSWORD = environ["DATABASE_PASSWORD"]
DATABASE = "employees"

engine = create_engine("mysql+pymysql://{}:{}@localhost/{}".format(USER, PASSWORD, DATABASE))
session_factory = sessionmaker(bind=engine)
