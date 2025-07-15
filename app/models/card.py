from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func

from app.db.database import Base


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    image = Column(String, nullable=False)  # Image URL for the miner
    cost = Column(Integer, default=1)  # Cost of the miner
    cycle_time = Column(Integer, default=4)  # Cycle time in hours
    frozen = Column(Boolean, default=False)  # Indicates if the miner is frozen
    buy = Column(Boolean, default=True)  # Indicates if the miner is available for purchase
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Card(id={self.id}, name={self.name})>"