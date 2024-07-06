from typing import NoReturn, Annotated
from fastapi import HTTPException, status, Request, Header, Depends
from sqlalchemy.exc import NoResultFound

from utils.hmac_signature import validate_signature
from services.users import UserServices
from schemas.users import UserSchema
from api.dependencies.db import UowDependency


def get_tg_chat_id(tg_chat_id: Annotated[str | int, Header(title='User chat_id in tg')]) -> str:
    return str(tg_chat_id)


def get_tg_hmac_signature(hmac_signature: Annotated[str, Header(title='Request signature')]) -> str:
    return hmac_signature


async def tg_get_user(tg_chat_id: Annotated[str, Depends(get_tg_chat_id)],
                      uow: UowDependency) -> UserSchema | NoReturn:
    try:
        user = await UserServices.get_user(uow, chat_id=tg_chat_id)
        return user
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No user with provided chat_id')


async def tg_verify_signature(tg_chat_id: Annotated[str, Depends(get_tg_chat_id)],
                              hmac_signature: Annotated[str, Depends(get_tg_hmac_signature)],
                              request: Request) -> None | NoReturn:
    body = await request.body()
    raw_data_for_signature = f'{tg_chat_id}'.encode()\
                              + b'\r\n\r\n'\
                              + body
    if not validate_signature(hmac_signature, raw_data_for_signature):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid request signature')
    

UserDependency = Annotated[UserSchema, Depends(tg_get_user)]
