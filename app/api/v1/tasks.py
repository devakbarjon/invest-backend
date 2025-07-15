from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from app.db.database import get_db
from app.models.schemas.tasks import TaskOut, TaskBase
from app.models.task import Task

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)

# Get all tasks for user
@router.get("/", response_model=list[TaskOut])
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

# Get single post by ID
@router.get("/{task_id}", response_model=PostOut)
async def get_post(task_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    stmt = select(Post).options(selectinload(Post.comments)).filter(Post.id == post_id)
    
    result = await db.execute(stmt)
    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if anon_id not in post.viewed_users:
        post.views += 1
        post.viewed_users = post.viewed_users + [anon_id]
    
    db.add(post)
    await db.commit()
    await db.refresh(post)

    return post