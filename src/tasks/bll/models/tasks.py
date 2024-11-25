from pydantic import BaseModel

from tasks.const import TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: str | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus

    class Config:
        orm_mode = True
        from_attributes = True
