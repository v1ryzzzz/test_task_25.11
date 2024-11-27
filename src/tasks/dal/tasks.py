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
        """Get task by id.

        Args:
            task_id: Task id.

        Returns:
            Task by id.

        Raises:
            HTTPException: If task not found
        """
        query = select(Task).where(Task.id == task_id)
        result = await self.db.execute(query)
        task = result.scalars().first()

        if not task:
            raise HTTPException(status_code=404, detail='Task not found')

        return task

    async def _get_tasks(self) -> List[Task]:
        """Get all tasks.

        Returns:
            All tasks.
        """
        query_result = await self.db.scalars(select(Task))
        tasks = query_result.all()
        return tasks

    async def create_task(
            self,
            task: TaskCreate,
    ) -> TaskResponse:
        """Create task. Send task to broker.

        Args:
            task: Task create schema.

        Returns:
            New task.
        """
        new_task = Task(title=task.title, description=task.description)
        self.db.add(new_task)
        await self.db.commit()
        await self.db.refresh(new_task)
        return TaskResponse.from_orm(new_task)

    async def get_task(
            self,
            task_id: int,
    ) -> TaskResponse:
        """Get task by id.

        Args:
            task_id: Task id.

        Returns:
            Task by id.
        """
        task = await self._get_task(task_id)
        return TaskResponse.from_orm(task)

    async def get_tasks(
            self,
    ) -> List[TaskResponse]:
        """Get all tasks.

        Returns:
            All tasks.
        """
        tasks = await self._get_tasks()
        return [TaskResponse.from_orm(task) for task in tasks]
