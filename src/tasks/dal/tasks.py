from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tasks.bll.models.tasks import TaskResponse, TaskCreate
from tasks.bll.tasks import AbstractTasksStorage
from tasks.dal.models.tasks import Task


class TasksStorage(AbstractTasksStorage):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _get_task(self, task_id: int) -> Task:
        query = select(Task).where(Task.id == task_id)
        result = await self.db.execute(query)
        task = result.scalars().first()

        if not task:
            raise HTTPException(status_code=404, detail='Task not found')

        return task

    async def _get_tasks(self) -> List[Task]:
        query_result = await self.db.scalars(select(Task))
        tasks = query_result.all()
        return tasks

    async def create_task(
            self,
            task: TaskCreate,
    ) -> TaskResponse:
        new_task = Task(title=task.title, description=task.description)
        self.db.add(new_task)
        await self.db.commit()
        await self.db.refresh(new_task)
        return TaskResponse.from_orm(new_task)

    async def get_task(
            self,
            task_id: int,
    ) -> TaskResponse:
        task = await self._get_task(task_id)
        return TaskResponse.from_orm(task)

    async def get_tasks(
            self,
    ) -> List[TaskResponse]:
        tasks = await self._get_tasks()
        return [TaskResponse.from_orm(task) for task in tasks]
