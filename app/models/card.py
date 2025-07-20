from sqlalchemy import Column, Integer, String, DateTime, Boolean, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    image = Column(String, nullable=False)  # Image URL for the miner
    cost = Column(Integer, default=1)  # Cost of the miner
    cycle_reward = Column(Numeric, default=0.02)  # Reward per cycle
    cycle_time = Column(Integer, default=4)  # Cycle time in hours
    frozen = Column(Boolean, default=False)  # Indicates if the miner is frozen
    profit = Column(Integer, default=5)  # Total profit from the miner in percentage
    buy = Column(Boolean, default=True)  # Indicates if the miner is available for purchase
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user_cards = relationship(
        "UserCard",
        back_populates="card",
        cascade="all, delete-orphan"
    )

    def __init__(self, 
                 name: str, 
                 image: str, 
                 cost: int = 1, 
                 cycle_reward: float = 0.02, 
                 cycle_time: int = 4,
                 profit: int = 5,
                 frozen: bool = False, 
                 buy: bool = True):
        self.name = name
        self.image = image
        self.cost = cost
        self.cycle_reward = cycle_reward
        self.cycle_time = cycle_time
        self.profit = profit
        self.frozen = frozen
        self.buy = buy

    def __repr__(self):
        return f"<Card(id={self.id}, name={self.name})>"