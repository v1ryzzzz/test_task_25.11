from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from tasks.bll import TasksBLL
from tasks.bll.models.tasks import TaskResponse, TaskCreate
from tasks.dal import TasksDAL

router = APIRouter(tags=['Tasks'])


@router.post('/tasks', response_model=TaskResponse)
async def create_task(
        task: TaskCreate,
        db: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> TaskResponse:
    tasks_service = TasksBLL.tasks_service(storage=TasksDAL.tasks_storage(db=db))
    return await tasks_service.create_task(task)


@router.get('/tasks/{task_id}', response_model=TaskResponse)
async def get_task(
        task_id: int,
        db: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> TaskResponse:
    tasks_service = TasksBLL.tasks_service(storage=TasksDAL.tasks_storage(db=db))
    return await tasks_service.get_task(task_id)


@router.get('/tasks', response_model=List[TaskResponse])
async def get_tasks(
        db: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> List[TaskResponse]:
    tasks_service = TasksBLL.tasks_service(storage=TasksDAL.tasks_storage(db=db))
    return await tasks_service.get_tasks()
