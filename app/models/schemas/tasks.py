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
    completed: bool = Field(False, example=False)  # Indicates if the task is completed
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
        use_enum_values = True  # If using enums in your model, this will serialize them as their values