import abc
from typing import List

from logger.logger import logger

from kafka_client.kafka_producer import send_task_to_kafka
from rabbitmq_client.rabbitmq_producer import send_task_to_rabbitmq
from tasks.bll.models.tasks import TaskResponse, TaskCreate
from tasks.const import Broker


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
        """Create task. Send task to broker.

        Args:
            task: Task create schema.

        Returns:
            New task.
        """
        new_task = await self.storage.create_task(task)
        if task.broker == Broker.rabbitmq:
            await send_task_to_rabbitmq(new_task.id)
            logger.info('Task sent to rabbitmq.')
        else:
            await send_task_to_kafka(new_task.id)
            logger.info('Task sent to kafka.')
        return new_task

    async def get_task(self, task_id: int) -> TaskResponse:
        """Get task by id.

        Args:
            task_id: Task id.

        Returns:
            Task by id.
        """
        return await self.storage.get_task(task_id)

    async def get_tasks(self) -> List[TaskResponse]:
        """Get all tasks.

        Returns:
            All tasks.
        """
        return await self.storage.get_tasks()
