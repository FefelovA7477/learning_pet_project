from services.repositories.base_repository import BaseRepository
from models.tasks import Task


class TaskRepo(BaseRepository):
    model = Task