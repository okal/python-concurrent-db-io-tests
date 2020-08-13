import aiomysql
import asyncio

from db import USER, PASSWORD, DATABASE, queries

loop = asyncio.get_event_loop()


async def execute_query(query, pool):
    async with pool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(query)
            result = await cursor.fetchall()
            print(result[0])
            print(len(result))


async def run():
    pool = await aiomysql.create_pool(
        host="localhost", port=3306, user=USER, password=PASSWORD, db=DATABASE
    )

    tasks = [execute_query(query, pool) for query in queries]
    await asyncio.gather(*tasks)

loop.run_until_complete(run())