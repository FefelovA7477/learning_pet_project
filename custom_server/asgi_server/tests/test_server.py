import asyncio
import socket
from multiprocessing import Queue as MPQueue
from functools import partial

from asgi_server.server.worker import WorkerPool
from asgi_server.asgi.http_asgi import ASGIHTTP


async def test_worker():
    test_queue = MPQueue()

    def generate_port():
        for i in range(57432, 57442):
            yield i

    async def add_socket_to_q(q: MPQueue) -> None:
        for port in generate_port():
            new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new_socket.bind(('127.0.0.1', port))
            new_socket.setblocking(False)
            await asyncio.to_thread(partial(test_queue.put, new_socket))
            print('sock added')
            await asyncio.sleep(2)

    new_pool = WorkerPool(test_queue)
    workers = asyncio.get_running_loop().create_task(new_pool.run_workers(
        ASGIHTTP
    ))
    await add_socket_to_q(test_queue)
    await workers