from typing import NamedTuple, Dict, Callable, Any


class HTTPMeta(NamedTuple):
    raw_http_version: bytes
    raw_method: bytes
    raw_full_path: bytes
    raw_headers: Dict[bytes, bytes]
    raw_scheme: bytes


class HTTPRawRequest(NamedTuple):
    raw_meta: bytes
    body: bytes = b''


class AppParams(NamedTuple):
    scope: Dict[str, Any]
    receive: Callable[[], Dict[str, Any]]
    send: Callable[[Dict[str, Any]], None]