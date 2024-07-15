from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv(dotenv_path=str(Path(__file__).resolve().parents[1]) + '/.env')

class Settings(BaseSettings):
    DB_URI: str
    API_SECRET: str
    DEBUG: int
    YANDEX_GPT_API_TOKEN: str
    YANDEX_GPT_CATALOG_ID: str
    YANDEX_GPT_FOLDER_ID: str

    class Config:
        env_file = '.env'

settings = Settings()