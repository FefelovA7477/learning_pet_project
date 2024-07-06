# WARNING 
# Temporary importing asgi_server requestLogger
from logging import Logger
from asgi_server.log_sys.log import request_logger


def get_logger() -> Logger:
    return request_logger