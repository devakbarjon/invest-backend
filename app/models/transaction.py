from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Numeric
from sqlalchemy.sql import func

from app.db.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    sender = Column(String, nullable=True)
    amount = Column(Numeric(precision=20, scale=4), nullable=False)
    transaction_type = Column(String, nullable=False)  # Type of transaction (e.g., 'deposit', 'withdrawal')
    currency = Column(String, default='ton')
    status = Column(String, default='pending')  # Status of the transaction (e.g., 'pending', 'completed', 'failed')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, user_id: int, amount: float, transaction_type: str, status: str, currency: str = 'ton', sender: str = None,
                 transaction_id: str = None):
        self.user_id = user_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.status = status
        self.currency = currency
        self.sender = sender
        self.transaction_id = transaction_id

    def __repr__(self):
        return f"<Transaction(id={self.id}, user_id={self.user_id}, amount={self.amount}, type={self.transaction_type})>"