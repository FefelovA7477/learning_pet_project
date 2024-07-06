from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.config import settings


ENGINE = create_async_engine(url=settings.DB_URI)
DEFAULT_SESSION_FACTORY = async_sessionmaker(ENGINE, expire_on_commit=False)