import asyncio

from arq import create_pool
from job import my_function


async def main() -> None:
    pool = await create_pool()
    await pool.enqueue_job(my_function.__name__, 2)
    await pool.enqueue_job(my_function.__name__, 2)
    await pool.enqueue_job(my_function.__name__, 2)
    await pool.enqueue_job(my_function.__name__, 2)
    await pool.enqueue_job(my_function.__name__, 2)


if __name__ == '__main__':
    asyncio.run(main())
