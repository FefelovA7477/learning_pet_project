import abc
from typing import List
from multiprocessing import Process, Queue


class BaseServer(abc.ABC):
    _workers_pool: List[Process]
    _client_socket_queue: Queue
    
    @abc.abstractmethod
    async def start_server(self):
        raise NotImplementedError