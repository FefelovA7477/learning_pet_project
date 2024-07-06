import asyncio
import socket
from typing import Callable
from multiprocessing import Queue

from asgi_server.core.config import settings
from asgi_server.server.worker import WorkerPool
from asgi_server.log_sys.log import sys_logger


class Server:
    def __init__(self, workers_num: int | None = None) -> None:
        self._client_socket_queue = Queue()
        self._workers_pool = WorkerPool(client_socket_queue=self._client_socket_queue,
                                        pool_size=workers_num)

    async def start_server(self):
        server_socket = self._start_server_socket()
        self._workers_pool.run_workers()
        while True:
            self._client_socket_queue.put(await self._accept_client_connection(server_socket))
            sys_logger.debug('Client added to the queue.')

    async def _accept_client_connection(self, server_socket: socket.socket) -> socket.socket:
        client_socket, _ = await asyncio.get_running_loop().sock_accept(sock=server_socket)
        client_socket.setblocking(False)
        sys_logger.debug(f'Client accepted. Client socket: {client_socket}')
        return client_socket

    def _start_server_socket(self) -> socket.socket:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((settings.SERVERSOCKET_IP, settings.SERVERSOCKET_PORT))
        server_socket.listen()
        server_socket.setblocking(False)
        sys_logger.debug(f'Server started.')
        return server_socket
            