from typing import AsyncGenerator
from sqlalchemy import select
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
    from app.models.card import Card

    exist_cards = await db.execute(select(Card))
    exist_cards = exist_cards.scalars().all()
    if exist_cards:
        return  # Cards already exist, no need to create fake ones
    data = {
        1: {
            "name": "USDC",  # Топ 7
            "image": "https://example.com/card_1.png",
            "cost": 1,
            "cycle_reward": 0.02,
            "cycle_time": 2,
            "profit": 30,
            "frozen": False,
            "buy": True
        },
        2: {
            "name": "SOL",  # Топ 6
            "image": "https://example.com/card_2.png",
            "cost": 5,
            "cycle_reward": 0.04,
            "cycle_time": 4,
            "profit": 40,
            "frozen": False,
            "buy": True
        },
        3: {
            "name": "BNB",  # Топ 5
            "image": "https://example.com/card_3.png",
            "cost": 20,
            "cycle_reward": 0.4,
            "cycle_time": 6,
            "profit": 40,
            "frozen": False,
            "buy": True
        },
        4: {
            "name": "XRP",  # Топ 4
            "image": "https://example.com/card_4.png",
            "cost": 50,
            "cycle_reward": 1,
            "cycle_time": 6,
            "profit": 40,
            "frozen": False,
            "buy": True
        },
        5: {
            "name": "USDT",  # Топ 3
            "image": "https://example.com/card_5.png",
            "cost": 100,
            "cycle_reward": 2.5,
            "cycle_time": 8,
            "profit": 45,
            "frozen": False,
            "buy": True
        },
        6: {
            "name": "ETH",  # Топ 2
            "image": "https://example.com/card_6.png",
            "cost": 200,
            "cycle_reward": 5,
            "cycle_time": 12,
            "profit": 50,
            "frozen": False,
            "buy": True
        },
        7: {
            "name": "BTC",  # Топ 1
            "image": "https://example.com/card_7.png",
            "cost": 300,
            "cycle_reward": 7,
            "cycle_time": 12,
            "profit": 50,
            "frozen": False,
            "buy": True
        }
    }

    for card_id, card_data in data.items():
        card = Card(
            name=card_data["name"],
            image=card_data["image"],
            cost=card_data["cost"],
            cycle_reward=card_data["cycle_reward"],
            cycle_time=card_data["cycle_time"],
            profit=card_data["profit"],
            frozen=card_data["frozen"],
            buy=card_data["buy"]
        )
        db.add(card)
    await db.commit()
    await db.refresh(card)