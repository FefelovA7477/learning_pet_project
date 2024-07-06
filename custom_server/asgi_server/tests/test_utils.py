import asyncio

from asgi_server.utils.utils import tasks_logger_daemon


async def test_log_tasks():
    asyncio.create_task(tasks_logger_daemon(1), name='logging')
    async def create_random_io_bound():
        await asyncio.sleep(20)
    for _ in range(3):
        asyncio.create_task(create_random_io_bound(), name='io_bound')
        await asyncio.sleep(2)
    await asyncio.sleep(60)
    for task in asyncio.all_tasks():
        await task