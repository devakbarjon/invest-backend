from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy import any_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.schemas.tasks import TaskCheckIn, TaskOut, TaskCheck, TaskCompleted
from app.models.schemas.users import UserIn
from app.models.task import Task
from app.models.user import User
from app.services.bot.bot_auth import authenticate_user

router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"]
)

# Get all tasks for user
@router.get("/", response_model=list[TaskOut])
async def get_tasks(
    db: AsyncSession = Depends(get_db)
):
    """
    Return all tasks.
    """

    result = await db.execute(select(Task))
    tasks: list[Task] = result.scalars().all()

    return [TaskOut.model_validate(task, from_attributes=True) for task in tasks]

# Check is task completed for user
@router.post("/checkTasks", response_model=TaskCheck)
async def check_task(task_in: TaskCheckIn, db: AsyncSession = Depends(get_db)):
    """
    Check if the task is completed by the user.
    If not, add the user's id to the `users` array column.
    """

    init_data = task_in.initData
    user_id = task_in.user_id
    task_id = task_in.id

    user = await authenticate_user(
        init_data=init_data,
        user_id=user_id
    )

    if user.get("success") is False:
        raise HTTPException(status_code=400, detail=user.get("message", "Authentication failed"))
    
    user: User = user.get("user")

    task = await db.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if user_id not in (task.users or []):
        task.users = task.users + [user_id]
        await db.add(task)
        await db.commit()
        await db.refresh(task)

        user.balance_payments_ton += task.reward
        await db.add(user)
        await db.commit()
        await db.refresh(user)
    else:
        raise HTTPException(status_code=400, detail="Task already completed.")
    
    return TaskCheck(
        id=task.id,
        status=1
    )


@router.post("/getTasksUser", response_model=TaskCompleted)
async def get_tasks_user(
    user_in: UserIn,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all tasks completed by the user.
    """

    init_data = user_in.initData
    user_id = user_in.user_id

    user = await authenticate_user(
        init_data=init_data,
        user_id=user_id
    )

    if user.get("success") is False:
        raise HTTPException(status_code=400, detail=user.get("message", "Authentication failed"))
    
    user: User = user.get("user")

    result = await db.execute(
        select(Task).where(user_id == any_(Task.users))
    )
    
    tasks: list[Task] = result.scalars().all()

    completed_tasks = []

    for task in tasks:
        completed_tasks.append(
            {
                "id": task.id,
                "user_id": user_id,
                "tasks_id": task.id
            }
        )

    return TaskCompleted(tasks=completed_tasks)