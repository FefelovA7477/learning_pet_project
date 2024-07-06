import logging
from fastapi import Request
from typing import Callable

from asgi_server.log_sys.log import request_logger


async def log_into_server_logger(request: Request, call_next):
    request_logger.debug('smth')
    return await call_next(request)