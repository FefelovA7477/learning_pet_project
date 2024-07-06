from asyncio import StreamReader, StreamWriter
import socket
import asyncio

from asgi_server.core._app import app
from asgi_server.connections.protocols.http1x import HTTP1xProtocol
from asgi_server.connections.http1xcon import HTTPConnection
from asgi_server.log_sys.log import sys_logger
    

class ConnectionHandler:
    def __init__(self) -> None:
        # self._connections = []
        pass

    async def handle_connection(self, client_socket: socket.socket) -> None:
        sys_logger.debug('Handling connection...')
        loop = asyncio.get_running_loop()
        connection = await self._open_connection(client_socket=client_socket, loop=loop)
        # self._connections.append(connection)
        loop.create_task(connection.run_app(app))
        sys_logger.debug('Handling task created')

    async def _open_connection(self, client_socket: socket.socket, 
                               loop: asyncio.AbstractEventLoop = None) -> HTTPConnection:
        loop = loop or asyncio.get_running_loop()
        reader = StreamReader(loop=loop)
        protocol = HTTP1xProtocol(reader, loop=loop)
        transport, _ = await loop.create_connection(
            lambda: protocol, sock=client_socket)
        writer = StreamWriter(transport, protocol, reader, loop)
        connection = HTTPConnection(reader=reader, writer=writer)
        return connection
    
    # async def _run_middleware(self):
    #     pass

    # async def _get_connection_protocol(self):
    #     pass
        
