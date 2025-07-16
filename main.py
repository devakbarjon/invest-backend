from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine, Base, fake_cards_generator, get_db
from app.logging_config import logger
from app.api.v1 import tasks
from app.api.v1 import users

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database models initialized.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()  # Initialize database models
    async for db in get_db():
        await fake_cards_generator(db=db)
    yield 
    logger.info("Shutting down...")


app = FastAPI(lifespan=lifespan)

app.include_router(
    tasks.router, tags=["Tasks"]
)

app.include_router(
    users.router, tags=["Users"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url} {request.client.host}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response