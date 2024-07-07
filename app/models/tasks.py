import datetime
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base_class import Base
from schemas.tasks import TaskSchema, TaskStatusChoice


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    status_updated_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now, 
                                                                 onupdate=datetime.datetime.now)
    deadline: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    title: Mapped[str] = mapped_column(String[64])
    description: Mapped[str]
    status: Mapped[TaskStatusChoice]

    user: Mapped['User'] = relationship(back_populates='tasks')

    def to_read_model(self) -> TaskSchema:
        return TaskSchema(
            id=self.id,
            user_id=self.user_id,
            created_at=self.created_at,
            status_updated_at=self.status_updated_at,
            deadline=self.deadline,
            title=self.title,
            description=self.description,
            status=self.status
        )



