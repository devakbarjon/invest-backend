from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


# id = Column(Integer, primary_key=True, index=True)
# name = Column(String, nullable=False)
# image = Column(String, nullable=False)  # Image URL for the miner
# cost = Column(Integer, default=1)  # Cost of the miner
# cycle_reward = Column(Numeric, default=0.02)  # Reward per cycle
# cycle_time = Column(Integer, default=4)  # Cycle time in hours
# frozen = Column(Boolean, default=False)  # Indicates if the miner is frozen
# buy = Column(Boolean, default=True)  # Indicates if the miner is available for purchase
# created_at = Column(DateTime(timezone=True), server_default=func.now())
# updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class CardOut(BaseModel):
    id: int
    name: str
    image: str  # Image URL for the miner
    cost: int = Field(default=1, example=1)  # Cost of the miner
    cycle_reward: Decimal = Field(default=0.02, example=0.02)  # Reward per cycle
    cycle_time: int = Field(default=4, example=4)  # Cycle time in hours
    frozen: bool = Field(default=False, example=False)  # Indicates if the miner is
    buy: bool = Field(default=True, example=True)  # Indicates if the miner is available for purchase
    created_at: datetime

    class Config:
        orm_mode = True
        use_enum_values = True


class CardIn(BaseModel):
    user_id: int
    initData: str