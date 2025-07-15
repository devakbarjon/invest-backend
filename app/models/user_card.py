from sqlalchemy import Column, Integer, DateTime, Boolean, BigInteger, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base

class UserCard(Base):
    __tablename__ = "user_cards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    card_id = Column(Integer, ForeignKey('cards.id'), nullable=False)
    next_cycle = Column(DateTime(timezone=True), nullable=False)  # Next cycle time for the card
    income = Column(Numeric(precision=20, scale=4), default=0.0)  # Income from the card
    status = Column(Boolean, default=True)  # Indicates if the card is active
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="user_cards")
    card = relationship("Card", back_populates="user_cards")

    def __repr__(self):
        return f"<UserCard(user_id={self.user_id}, card_id={self.card_id})>"