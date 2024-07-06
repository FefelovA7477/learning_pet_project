import asyncio
import socket
import os
from typing import Callable
from multiprocessing import Queue
from multiprocessing import Process

from asgi_server.log_sys.log import sys_logger
from asgi_server.utils.utils import tasks_logger_daemon
from asgi_server.connections.connection_handler import ConnectionHandler


def log_debug_status(msg: str, **kwargs) -> None:
    msg = str(msg)
    msg += f' Worker PID: {os.getpid()}'
    if 'socket' in kwargs.keys():
        msg += f', client socket: {kwargs['socket']}'
    sys_logger.debug(msg,)


class WorkerPool:
    def __init__(self, client_socket_queue: Queue, pool_size: int | None = None) -> None:
        """
        :param pool_size: os.cpu_count() as default
        """
        self._workers_pool = []
        if pool_size is None:
            pool_size = os.cpu_count()
        for _ in range(pool_size):
            self._workers_pool.append(Worker(client_socket_queue=client_socket_queue))

    def run_workers(self) -> None:
        for worker in self._workers_pool:
            worker.start()
    
    def peaceful_shutdown(self) -> None:
        for worker in self._workers_pool:
            worker.join(timeout=5)


class Worker(Process):
    def __init__(self, client_socket_queue: Queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection_handler = ConnectionHandler()
        self.client_socket_queue = client_socket_queue

    def run(self) -> None:
        self.start_worker()

    def start_worker(self) -> None:
        asyncio.run(self.handle_client_queue())

    async def handle_client_queue(self) -> None:
        asyncio.create_task(tasks_logger_daemon(120))
        log_debug_status('Worker started.')
        while True:
            client_socket = await asyncio.to_thread(self.client_socket_queue.get)
            log_debug_status('Client socket received by worker.')
            await self.start_client_session(client_socket=client_socket)

    async def start_client_session(self, client_socket: socket.socket) -> None:
        await self.connection_handler.handle_connection(client_socket=client_socket)