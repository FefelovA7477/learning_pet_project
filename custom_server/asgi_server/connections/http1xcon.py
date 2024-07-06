import asyncio
from http.client import responses
from typing import Callable, Any, Dict, Awaitable

from asgi_server.utils.types import AppParams, HTTPMeta, HTTPRawRequest
from asgi_server.log_sys.log import request_logger


class HTTPConnection:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        self.stream_writer = writer
        self.stream_reader = reader

    async def run_app(self, app: Callable[[AppParams], Awaitable[None]]) -> None:
        await self._process_request()
        try:
            res = await app(scope=self.scope, receive=self.receive, send=self.send)
            request_logger.debug(f'App work ended. Return: {res}')
        except Exception as e:
            request_logger.critical(f'App error: {e}')

    async def send(self, message: Dict[str, Any]) -> None:
        raw_message = HTTP1xRequestUtils.encode_send_message(message, self.scope['http_version'])
        self.stream_writer.write(raw_message)
        if message['type'] == 'http.response.body' and not message.get('more_body', False):
            await self.stream_writer.drain()
            self.stream_writer.close()
            await self.stream_writer.wait_closed()
    
    async def receive(self) -> Dict[str, Any]:
        request_logger.debug('Receive method called.')
        return {
            'type': 'http.request',
            'body': self.body,
            'more_body': False
        }
    
    async def _process_request(self) -> None:
        raw_request_data = await self._read_request()
        request_meta = HTTP1xRequestUtils.parse_http_meta(raw_request_data.raw_meta)
        self.scope = HTTP1xRequestUtils.get_scope(parsed_data=request_meta)
        self.body = raw_request_data.body

    async def _read_request(self) -> HTTPRawRequest:
        request_logger.debug('Reading request...')
        raw_data = b''
        body_size = 0
        while (data := await self.stream_reader.readline()):
            request_logger.debug(f'data chunk received: {data}')
            raw_data += data
            if data in [b'\r\n', b'\n']:
                break
            elif b'Content-Length' in data:
                body_size = int(data.split(b': ', 1)[1])
        body = await self._read_request_body(body_size)
        request_logger.debug(f'Request was read: {raw_data}, body: {body}')
        return HTTPRawRequest(raw_meta=raw_data, body=body)
    
    async def _read_request_body(self, content_length: int) -> bytes:
        request_logger.debug('Reading body...')
        try:
            body = await self.stream_reader.readexactly(content_length)
            request_logger.debug(f'Body received! Body: {body}')
            return body
        except Exception as e:
            request_logger.error(e)


class HTTP1xRequestUtils:
    @staticmethod
    def encode_send_message(message: Dict[str, Any], https_version: str = '1.1') -> bytes:
        if message['type'] == 'http.response.start':
            status = message['status']
            response_headers = '\r\n'.join(
                [f'{k.decode()}: {v.decode()}' for k, v in message['headers']]
            )
            response_phrase = HTTP1xRequestUtils._get_response_phrase(status)
            raw_message = f'HTTP/{https_version} {status} {response_phrase}\r\n{response_headers}\r\n\r\n'.encode('utf-8')
        elif message['type'] == 'http.response.body':
            raw_message = message['body']
        else:
            raw_message = b''
        request_logger.debug(f'writed raw: {raw_message}')
        return raw_message
    
    @staticmethod
    def _get_response_phrase(status_code: int) -> str:
        return responses[status_code]
    
    @staticmethod
    def _capitalize_hyphenated_header(header: str):
        return '-'.join(word.capitalize() for word in header.split('-'))

    @staticmethod
    def get_scope(parsed_data: HTTPMeta) -> Dict[str, Any]:
        try:
            raw_path, _, raw_query = parsed_data.raw_full_path.partition(b'?')
            scope = {
                'type': 'http',
                'asgi': {
                    'version': '2.0',
                },
                'http_version': parsed_data.raw_http_version[-3:].decode(),
                'method': parsed_data.raw_method.decode(),
                'scheme': parsed_data.raw_scheme.decode(),
                'path': raw_path.decode(),
                'raw_path': raw_path,
                'query_string': raw_query,
                'headers': parsed_data.raw_headers,
            }
        except Exception as e:
            request_logger.error(e)
        request_logger.debug(f'scope formatted: {scope}')
        return scope
               
    @staticmethod
    def parse_http_meta(raw_data: bytes) -> HTTPMeta:
        meta, _ = raw_data.split(b'\r\n\r\n', 1)
        meta = meta.split(b'\r\n')
        raw_method, raw_full_path, raw_version = meta[0].split(b' ')
        raw_headers = [tuple(line.lower().split(b': ', 1)) for line in meta[1:]]
        parsed_data = HTTPMeta(
            raw_http_version=raw_version,
            raw_method=raw_method,
            raw_full_path=raw_full_path,
            raw_headers=raw_headers,
            raw_scheme=b'http'
        )
        request_logger.debug(f'Data decomposed. Data: {parsed_data}')
        return parsed_data