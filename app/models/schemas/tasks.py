from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from app.models.task import Task

class TaskBase(BaseModel):
    name: str = Field(..., example="Task Name")
    description: Optional[str] = Field(None, example="This is a task description.")
    link: str = Field(..., example="https://example.com/task-link")
    icon: Optional[str] = Field(None, example="https://example.com/icon.png")
    pin: bool = Field(True, example=True)
    type: str = Field(..., example="main")  # e.g., 'main', 'partner'


class TaskOut(TaskBase):
    id: int
    status: bool = Field(True, example=True)
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
        use_enum_values = True


class TaskCheckIn(TaskBase):
    user_id: int = Field(..., example=1)
    initData: str
    id: int = Field(..., example=1, description="Task ID to check")

class TaskCheck(BaseModel):
    id: int = Field(..., example=1)
    status: int = Field(1, example=1)