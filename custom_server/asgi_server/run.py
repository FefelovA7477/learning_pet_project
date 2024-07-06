from asgi_server.server.server import Server
from asgi_server.asgi.http_asgi import ASGIHTTP


def run():
    server = ASGIHTTP(Server)
    server.run_asgi()