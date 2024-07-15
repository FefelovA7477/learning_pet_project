from fastapi import APIRouter, status, Path, Body, HTTPException
from typing import List, Annotated

from schemas.tasks import TaskSchemaInfo, TaskSchemaUpdate, TaskShemaAdd
from schemas.users import UserSchema
from services.tasks import TaskServices
from api.dependencies.db import UowDependency
from api.dependencies.tg import UserDependency
from yandexgpt.api import get_task_from_msg
from yandexgpt.exc import TaskExtractError


tasks_router = APIRouter(
    prefix='/tasks',
    tags=['Tasks']
)


@tasks_router.get('/')
async def get_user_tasks(uow: UowDependency, user: UserDependency) -> List[TaskSchemaInfo]:
    tasks = await TaskServices.get_user_tasks(uow, user_id=user.id)
    return tasks


@tasks_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_task(uow: UowDependency, user: UserDependency,
                      task: TaskShemaAdd) -> TaskSchemaInfo:
    task = await TaskServices.create_task(uow, task, user.id)
    return task


@tasks_router.post('/tg', status_code=status.HTTP_201_CREATED)
async def create_task_from_msg(uow: UowDependency, user: UserDependency,
                               msg: Annotated[str, Body(embed=True)]) -> TaskSchemaInfo:
    try:
        task_schema = await get_task_from_msg(user_msg=msg)
    except TaskExtractError:
        raise HTTPException(status_code=400, detail='Cant extract task from provided msg')
    task = await TaskServices.create_task(uow, task_schema, user.id)
    return task


@tasks_router.get('/{task_id}')
async def get_task(uow: UowDependency, task_id: Annotated[int, Path(title='ID of the task')]) -> TaskSchemaInfo:
    task = await TaskServices.get_task(uow, id=task_id)
    return task


@tasks_router.patch('/{task_id}', status_code=status.HTTP_206_PARTIAL_CONTENT)
async def update_task(uow: UowDependency, task_id: Annotated[int, Path(title='ID of the task')], 
                      update_values: TaskSchemaUpdate) -> int:
    updated = await TaskServices.update_task(uow=uow, task_id=task_id, 
                                       update_values=update_values)
    return updated