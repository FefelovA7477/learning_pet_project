import enum
from pydantic import BaseModel
from datetime import datetime


class TaskStatusChoice(enum.Enum):
    BACKLOG = 'backlog'
    IN_PROGRESS = 'in progress'
    DONE = 'done'
    EXPIRED = 'expired'


class TaskSchema(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    status_updated_at: datetime
    deadline: datetime
    title: str
    description: str
    status: TaskStatusChoice

    class Config:
        from_attributes = True 


class TaskShemaAdd(BaseModel):
    deadline: datetime
    title: str
    description: str
    status: TaskStatusChoice


class TaskSchemaInfo(BaseModel):
    created_at: datetime
    status_updated_at: datetime
    deadline: datetime
    title: str
    description: str
    status: TaskStatusChoice


class TaskSchemaUpdate(BaseModel):
    deadline: datetime | None = None
    title: str | None = None
    description: str | None = None
    status: TaskStatusChoice | None = None