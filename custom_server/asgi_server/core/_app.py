import sys
import importlib

from asgi_server.core.config import settings

def _setup_app() -> None:
    sys.path.insert(0, settings.APP_ROOT_PATH)
    module_str, _, attr_str = settings.APP_ATTR_PATH.partition(":")
    module = importlib.import_module(module_str)
    instance = getattr(module, attr_str)
    global app
    app = instance

_setup_app()