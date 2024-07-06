import os
import sys
from pathlib import Path
from typing import Callable
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / '.env')

class Settings(BaseSettings):
    SERVERSOCKET_IP: str = '127.0.0.1'
    SERVERSOCKET_PORT: int = 8000
    APP_ATTR_PATH: str 
    # = 'main:app'
    APP_ROOT_PATH: str 
    # = '/Users/fefa7477/Desktop/Dev/projects/dayplanner/app'

    class Config:
        env_file = '.env'

settings = Settings()