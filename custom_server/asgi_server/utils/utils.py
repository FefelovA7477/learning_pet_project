import asyncio
import os

from asgi_server.log_sys.log import sys_logger


async def tasks_logger_daemon(delay: int):
    while True:
        tasks_status = f'Process: {os.getpid()}. Pending tasks: '\
            + ', '.join(task.get_name() for task in asyncio.all_tasks())
        sys_logger.debug(tasks_status)
        await asyncio.sleep(delay)