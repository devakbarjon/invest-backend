from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, nullable=False, unique=True)  # Unique user identifier
    login = Column(String, nullable=True)
    lang = Column(String, nullable=True)  # User's language [ru, en, ua]
    balance_ton = Column(Numeric(precision=20, scale=4), default=0.0)  # User's TON balance
    balance_stars = Column(Numeric(precision=20, scale=4), default=0.0)  # User's Stars balance
    balance_payments_ton = Column(Numeric(precision=20, scale=4), default=0.0)  # User's TON payments balance
    avatar_url_telegram = Column(String, nullable=True)  # User's Telegram avatar URL
    referrer_id_level1 = Column(BigInteger, nullable=True)  # Referrer ID for level 1
    referrer_id_level2 = Column(BigInteger, nullable=True)  # Referrer ID
    referrer_id_level3 = Column(BigInteger, nullable=True)  # Referrer ID for level 3
    referral_count_level1 = Column(Integer, default=0)  # Count of level 1 referrals
    referral_count_level2 = Column(Integer, default=0)  # Count of level 2 referrals
    referral_count_level3 = Column(Integer, default=0)  # Count of level 3 referrals
    referral_income_level1 = Column(Numeric(precision=20, scale=4), default=0.0)  # Income from level 1 referrals
    referral_income_level2 = Column(Numeric(precision=20, scale=4), default=0.0)  # Income from level 2 referrals
    referral_income_level3 = Column(Numeric(precision=20, scale=4), default=0.0)  # Income from level 3 referrals
    withdrawal_ton = Column(Numeric(precision=20, scale=4), default=0.0)  # Withdrawal amount in TON
    deposit_ton = Column(Numeric(precision=20, scale=4), default=0.0)  # Deposit amount in TON
    deposit_stars = Column(BigInteger, default=0)  # Deposit amount in Stars
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user_cards = relationship(
        "UserCard",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __init__(self, 
                 user_id: int, 
                 login: str = None, 
                 lang: str = None, 
                 avatar_url_telegram: str = None,
                 referrer_id_level1: int = None,
                 referrer_id_level2: int = None,
                 referrer_id_level3: int = None
                 ):
        self.user_id = user_id
        self.login = login
        self.lang = lang
        self.avatar_url_telegram = avatar_url_telegram
        self.referrer_id_level1 = referrer_id_level1
        self.referrer_id_level2 = referrer_id_level2
        self.referrer_id_level3 = referrer_id_level3

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"