from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.schemas.tasks import TaskOut, TaskCheck
from app.models.task import Task

router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"]
)

# Get all tasks for user
@router.post("/", response_model=list[TaskOut])
async def get_tasks(
    db: AsyncSession = Depends(get_db),
    x_init_data: int = Header(..., alias="X-init-data"),   #  <‑‑ Init data for authentication
):
    """
    Return all tasks.
    Add `completed=True` if this user's id is in the `users` array column.
    """

    result = await db.execute(select(Task))
    tasks: list[Task] = result.scalars().all()

    for task in tasks:
        task.completed = x_init_data in (task.users or [])

    return tasks

# Check is task completed for user
@router.post("/{task_id}", response_model=TaskCheck)
async def check_task(task_id: int, db: AsyncSession = Depends(get_db), 
                     x_init_data: int = Header(..., alias="X-init-data")):
    """
    Check if the task is completed by the user.
    If not, add the user's id to the `users` array column.
    """

    task = await db.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if x_init_data not in (task.users or []):
        task.users.append(x_init_data)
        await db.commit()
    else:
        raise HTTPException(status_code=400, detail="Task already completed.")
    
    return TaskCheck(id=task.id, completed=True)
