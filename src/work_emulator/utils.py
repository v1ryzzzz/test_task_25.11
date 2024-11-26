import asyncio
import random
from sqlalchemy.future import select

from tasks.const import TaskStatus
from tasks.dal.models.tasks import Task
from core.db_helper import db_helper


async def update_task_status(task_id: int, status: str) -> None:
    db = db_helper.get_scoped_session()
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalars().first()
    task.status = status
    await db.commit()


async def process_task(task_id: int) -> None:
    await update_task_status(task_id, TaskStatus.IN_PROGRESS.value)
    delay = random.randint(5, 10)
    await asyncio.sleep(delay)
    if random.random() < 0.8:
        await update_task_status(task_id, TaskStatus.COMPLETED.value)
    else:
        await update_task_status(task_id, TaskStatus.FAILED.value)
