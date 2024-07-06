from asgi_server.log_sys.log import sys_logger, request_logger


def test_logging():
    sys_logger.error('123')
    request_logger.debug('321')

if __name__ == '__main__':
    test_logging()