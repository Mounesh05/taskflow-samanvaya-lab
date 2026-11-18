from typing import Literal

from pydantic import BaseModel, Field

TaskStatus = Literal["todo", "in_progress", "done"]


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    priority: int = Field(default=3, ge=1, le=5)


class TaskUpdate(BaseModel):
    status: TaskStatus


class Task(BaseModel):
    id: str
    title: str
    priority: int
    status: TaskStatus = "todo"