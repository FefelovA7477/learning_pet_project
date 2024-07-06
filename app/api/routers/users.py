from fastapi import APIRouter, status, Body, Depends, Request
from typing import Annotated

from schemas.users import UserSchemaAdd, UserSchemaInfo
from services.users import UserServices
from api.dependencies.db import UowDependency
from api.dependencies.tg import UserDependency, get_tg_chat_id

from log.loggers import request_logger


user_router = APIRouter(
    prefix='/user',
    tags=['User'],
)


@user_router.get('/me')
async def get_user_info(user: UserDependency) -> UserSchemaInfo:
    return user


@user_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(uow: UowDependency, username: Annotated[str, Body(embed=True)],
                      tg_chat_id: Annotated[str, Depends(get_tg_chat_id)]) -> UserSchemaInfo:
    user_schema = UserSchemaAdd(username=username, chat_id=tg_chat_id)
    user = await UserServices.create_user(uow, user_schema)
    return user


@user_router.post('/test_asgi_server', status_code=status.HTTP_201_CREATED)
async def get_request_info(uow: UowDependency, username: Annotated[str, Body(embed=True)],
                           tg_chat_id: Annotated[str, Depends(get_tg_chat_id)],
                           request: Request) -> None:
    request_logger.info(f'{request.headers}')
    body = await request.body()
    request_logger.info(f'{body}') 