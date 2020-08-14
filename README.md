Tests the relative performance of different concurrent DB access methods

#Test

Benchmarking was done using [hyperfine](https://github.com/sharkdp/hyperfine).
Test data was seeded from the employee database from https://github.com/datacharmer/test_db.

The below query was used, with the `LIKE` pattern being generated from the alphabet (26 queries).
It was designed to incorporate joins, sub-selects and a basic aggregation in order to approximate
real world complexity.

```mysql
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
```

Scenarios

### Single threaded.
source: `src/test_single.py`

```
Benchmark #1: python test_single.py
  Time (mean ± σ):     17.746 s ±  0.442 s    [User: 2.370 s, System: 0.205 s]
  Range (min … max):   17.359 s … 18.781 s    10 runs
```

### Multi-threaded
source: `src/test_mt.py`
```
Benchmark #1: python test_mt.py
  Time (mean ± σ):      8.054 s ±  0.640 s    [User: 4.481 s, System: 1.782 s]
  Range (min … max):    7.148 s …  9.526 s    10 runs
```

### Multi-threaded with BoundedSemaphore.
source: `src/test_mt_bounded.py`

```
Benchmark #1: python test_mt_bounded.py
  Time (mean ± σ):      8.275 s ±  1.053 s    [User: 4.298 s, System: 1.269 s]
  Range (min … max):    6.798 s … 10.541 s    10 runs
```
### Using concurrent.futures with ProcessingPoolExecutor
source: `src/test_cfp.py`

My naive implementation is broken. I haven't yet figured out how to pass along a SQLAlchemy session
to the query executor operating in a different process. The thread-local session can't be pickled.

I might not pursue this further, since my other investigations have shown that multiprocessing
is a bad fit for speeding upI/O, but potentially a good fit for speeding up heavy, parallelizable computation.
The communication overhead between the different processes (pickling/unpickling) takes away a lot of the
benefits of parallelization.

### Using concurrent.futures with Threadpool
source: `src/test_cft.py`

```
Benchmark #1: python test_cft.py
  Time (mean ± σ):      7.806 s ±  1.284 s    [User: 4.155 s, System: 1.232 s]
  Range (min … max):    6.637 s … 10.521 s    10 runs
```

### Using asyncio
source: `src/test_asyncio.py`

```
Benchmark #1: python test_asyncio.py
  Time (mean ± σ):      7.642 s ±  0.947 s    [User: 3.571 s, System: 0.134 s]
  Range (min … max):    6.380 s …  9.654 s    10 runs
```
