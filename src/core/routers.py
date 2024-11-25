from fastapi import APIRouter

from core.config import API_PREFIX
from tasks.api.tasks import router as tasks_router

router = APIRouter(prefix=API_PREFIX)


router.include_router(tasks_router)
