from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_serializer


class CardOut(BaseModel):
    id: int
    name: str
    image: str  # Image URL for the card
    cost: int = Field(default=1, example=1)  # Cost of the card
    cycle_reward: Decimal = Field(default=0.02, example=0.02)  # Reward per cycle
    cycle_time: int = Field(default=4, example=4)  # Cycle time in hours
    profit: int = Field(default=5, example=5)  # Total profit from the card in percentage
    frozen: bool = Field(default=False, example=False)  # Indicates if the card is
    buy: bool = Field(default=True, example=True)  # Indicates if the card is available for purchase
    created_at: datetime

    @field_serializer('cycle_reward')
    def format_cycle_reward(self, value: Decimal, _info):

        return f"{value:.4f}"

    class Config:
        orm_mode = True
        use_enum_values = True
        from_attributes = True


class CardIn(BaseModel):
    user_id: int
    initData: str