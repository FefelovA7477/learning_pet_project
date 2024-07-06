import hmac
import base64
import hashlib

from core.config import settings

__bytes_secret = bytes(settings.API_SECRET, 'utf-8')


def validate_signature(signature: str, request_raw_data: bytes) -> bool:
    r"""
    :param request_raw_data: format - b'{chat_id}\r\n\r\n{body}'
    """
    if settings.DEBUG:
        return True
    etalon_signature = _generate_signature(secret=__bytes_secret, request_raw_data=request_raw_data)
    return signature == etalon_signature


def _generate_signature(secret: bytes, request_raw_data: bytes) -> str:
    r"""
    :param request_raw_data: format - b'{chat_id}\r\n\r\n{body}'

    :return: signature in utf-8
    """
    signature = (base64.b64encode(hmac.new(secret, request_raw_data, digestmod=hashlib.sha256)
                                  .digest())
                                  .decode('utf-8'))
    return signature