from pydantic import BaseModel, validators
from typing import List


class UserSchema(BaseModel):
    id: int
    username: str
    chat_id: str

    class Config:
        from_attributes = True


class UserSchemaAdd(BaseModel):
    username: str
    chat_id: str


class UserSchemaInfo(BaseModel):
    username: str