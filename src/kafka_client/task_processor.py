import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from tasks.const import TaskStatus
from tasks.dal.models.tasks import Task


async def process_task(task: Task, db: AsyncSession):
    task.status = TaskStatus.IN_PROGRESS
    await db.commit()
    await asyncio.sleep(5)
    task.status = TaskStatus.COMPLETED
    await db.commit()
