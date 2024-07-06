import abc
from typing import Callable
from sqlalchemy.orm import Session

from db.db_init import DEFAULT_SESSION_FACTORY
from services.repositories.base_repository import BaseRepository


class BaseUOW(abc.ABC):
    session_factory: Callable[[], Session]
    
    def __init__(self) -> None:
        self.session_factory = DEFAULT_SESSION_FACTORY

    @abc.abstractmethod
    async def __aenter__(self) -> None:
        """
        Declare repositories as object attrs
        """
        pass

    async def __aexit__(self, *args) -> None:
        await self.session.rollback()
        await self.session.close()

    async def flush(self) -> None:
        await self.session.flush()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    


