from services.repositories.base_repository import BaseRepository
from models.user import User


class UserRepo(BaseRepository):
    model = User