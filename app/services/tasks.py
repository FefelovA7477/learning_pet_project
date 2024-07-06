from typing import List
from services.uow.usertasks import UserTaskUOW

from schemas.tasks import TaskShemaAdd, TaskSchema, TaskSchemaUpdate


class TaskServices:
    @staticmethod
    async def create_task(uow: UserTaskUOW, task: TaskShemaAdd, user_id: int) -> None:
        task_dump = task.model_dump()
        async with uow:
            task = await uow.tasks.create(user_id=user_id, **task_dump)
            await uow.commit()
        return task
            
    @staticmethod
    async def get_user_tasks(uow: UserTaskUOW, user_id: int) -> List[TaskSchema]:
        async with uow:
            user_tasks = await uow.tasks.filter(user_id=user_id)
        return user_tasks
    
    @staticmethod
    async def update_task(uow: UserTaskUOW, task_id: int, update_values: TaskSchemaUpdate) -> int:
        update_values = update_values.model_dump(exclude_unset=True)
        async with uow:
            updated = await uow.tasks.update({'id': task_id}, **update_values)
            await uow.commit()
        return updated
    
    @staticmethod
    async def get_task(uow: UserTaskUOW, **kwargs) -> TaskSchema: 
        async with uow:
            task = await uow.tasks.get(**kwargs)
        return task
