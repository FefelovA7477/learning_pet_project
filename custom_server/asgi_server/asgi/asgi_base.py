import abc
from typing import Callable, Type

from asgi_server.server.base_server import BaseServer


class ASGIBase(abc.ABC):
    @abc.abstractmethod
    def __init__(self, app: Callable, server_factory: Type[BaseServer]) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    def run_asgi(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def start_server(self):
        raise NotImplementedError
    
    