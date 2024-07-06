from typing import List, Any, Iterable, Dict
from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session
from pydantic import BaseModel

from db.base_class import Base


class BaseRepository:
    model: Base
    session: Session

    def __init__(self, db_session: Session, **kwargs):
        if self.model is None:
            raise AttributeError('Model attr should be declared')
        self.session = db_session
        
    async def create(self, **kwrags) -> None:
        stmnt = (
            insert(self.model)
            .values(**kwrags)
            .returning(self.model)
        )
        result = await self.session.execute(stmnt)
        return self._to_schema_repr(result.scalar_one())

    async def filter(self, *args, **kwargs) -> List[object]:
        stmnt = (
            select(self.model)
            .where(*args)
            .filter_by(**kwargs)
        )
        result = await self.session.execute(stmnt)
        return self._to_schema_repr(result.scalars().all())
    
    async def update(self, filter_by: Dict[str, Any], **kwargs) -> int:
        stmnt = (
            update(self.model)
            .values(**kwargs)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(stmnt)
        return result.rowcount

    async def get(self, *args, **kwargs) -> object:
        stmnt = (
            select(self.model)
            .where(*args)
            .filter_by(**kwargs)
        )
        result = await self.session.execute(stmnt)
        return self._to_schema_repr(result.scalar_one())
    
    async def execute_complex_stmnt(self, stmnt: Any) -> Any:
        result = await self.session.execute(stmnt)
        return self._to_schema_repr(result.scalars().all())
    
    def _to_schema_repr(self, data: Any) -> BaseModel | List[BaseModel]:
        if not hasattr(self.model, 'to_read_model'):
            raise AttributeError(f'No .to_read_model() declared in model: {self.model}')
        if isinstance(data, Iterable):
            return [record.to_read_model() for record in data]
        return data.to_read_model()
