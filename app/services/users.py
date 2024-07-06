from sqlalchemy.exc import NoResultFound

from schemas.users import UserSchemaAdd, UserSchemaInfo, UserSchema
from services.uow.usertasks import UserTaskUOW


class UserServices:
    @staticmethod
    async def create_user(uow: UserTaskUOW, user: UserSchemaAdd) -> UserSchema:
        user_dump = user.model_dump()
        async with uow:
            user = await uow.users.create(**user_dump)
            await uow.commit()
        return user
    
    @staticmethod
    async def get_user(uow: UserTaskUOW, **kwargs) -> UserSchema:
        async with uow:
            user = await uow.users.get(**kwargs)
        return user
    
    @staticmethod
    async def get_user_or_none(uow: UserTaskUOW, **kwargs) -> UserSchema | None:
        try:
            return await UserServices.get_user(uow, **kwargs)
        except NoResultFound:
            return None