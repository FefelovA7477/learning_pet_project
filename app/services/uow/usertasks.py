from services.uow.base_uow import BaseUOW
from services.repositories.tasks import TaskRepo
from services.repositories.users import UserRepo

class UserTaskUOW(BaseUOW):
    async def __aenter__(self) -> None:
        self.session = self.session_factory()
        self.users = UserRepo(self.session)
        self.tasks = TaskRepo(self.session)