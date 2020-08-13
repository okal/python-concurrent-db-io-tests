Tests the relative performance of different concurrent DB access methods

Test

1. Run a shared set of queries against the DB.
2. Return results in order, and time taken to execute all queries.

Scenarios

1. Single threaded.
2. Multi-threaded
3. Multi-threaded with BoundedSemaphore.
4. Multiprocessing with Pool of size `multiprocessing.cpu_count()`
5. Using concurrent.futures with Threadpool
6. Using asyncio
