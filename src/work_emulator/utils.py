import asyncio
import random
from sqlalchemy import select

from logger.logger import logger
from tasks.const import TaskStatus
from tasks.dal.models.tasks import Task
from core.db_helper import db_helper


async def update_task_status(task_id: int, status: str) -> None:
    db = db_helper.get_scoped_session()
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalars().first()
    task.status = status
    await db.commit()
    logger.info(
        'Task %s status updated', task_id
    )


async def process_task(task_id: int) -> None:
    logger.info('Starting processing for task %s', task_id)
    await update_task_status(task_id, TaskStatus.IN_PROGRESS.value)
    delay = random.randint(5, 10)
    await asyncio.sleep(delay)
    if random.random() < 0.8:
        new_status = TaskStatus.COMPLETED.value
    else:
        new_status = TaskStatus.FAILED.value

    await update_task_status(task_id, new_status)

    logger.info('Processing for task %s finished with status %s', task_id, new_status)
