from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create an async engine and session
engine = create_async_engine(settings.database_url, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()



async def fake_cards_generator(db: AsyncSession) -> None:
    pass
    # from app.models.card import Card
    # # Example of creating fake cards and user cards
    # for i in range(1, 8):
    #     card = Card(
    #         name=f"Card {i}",
    #         image=f"https://example.com/card_{i}.png",
    #         cost=i * 10,
    #         cycle_reward=0.01 * i,
    #         cycle_time=4 * i,
    #         frozen=False,
    #         buy=True 
    #     )
    #     db.add(card)
    #     await db.commit()
    #     await db.refresh(card)
    
    # await db.commit()