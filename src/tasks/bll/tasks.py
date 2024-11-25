import abc
from typing import List

from fastapi import HTTPException

from kafka_client.kafka_producer import send_task_to_kafka
from tasks.bll.models.tasks import TaskResponse, TaskCreate


class AbstractTasksStorage(abc.ABC):
    @abc.abstractmethod
    async def create_task(
            self,
            task: TaskCreate,
    ) -> TaskResponse:
        ...

    @abc.abstractmethod
    async def get_task(
            self,
            task_id: int,
    ) -> TaskResponse:
        ...

    @abc.abstractmethod
    async def get_tasks(
            self,
    ) -> List[TaskResponse]:
        ...


class TasksService:

    def __init__(
            self,
            storage: AbstractTasksStorage,
    ):
        self.storage = storage

    async def create_task(
            self,
            task: TaskCreate,
    ) -> TaskResponse:
        new_task = await self.storage.create_task(task)
        await send_task_to_kafka(new_task.id)
        return new_task

    async def get_task(self, task_id: int) -> TaskResponse:
        return await self.storage.get_task(task_id)

    async def get_tasks(self) -> List[TaskResponse]:
        return await self.storage.get_tasks()