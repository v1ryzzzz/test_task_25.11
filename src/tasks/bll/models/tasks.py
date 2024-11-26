from pydantic import BaseModel

from tasks.const import TaskStatus, Broker


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    broker: Broker


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus

    class Config:
        orm_mode = True
        from_attributes = True
