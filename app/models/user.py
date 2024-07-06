from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base_class import Base
from schemas.users import UserSchema


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(64))
    chat_id: Mapped[str] = mapped_column(String(32), unique=True)
    
    tasks: Mapped[List['Task']] = relationship(back_populates='user')

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            username=self.username,
            chat_id=self.chat_id
        )