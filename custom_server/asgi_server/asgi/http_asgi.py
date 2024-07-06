import asyncio
from typing import Type

from asgi_server.asgi.asgi_base import ASGIBase
from asgi_server.server.server import Server


class ASGIHTTP(ASGIBase):
    def __init__(self, server_factory: Type[Server]) -> None:
        self.server_factory = server_factory

    def run_asgi(self):
        asyncio.run(self.start_server())
    
    async def start_server(self):
        return await self.server_factory().start_server()