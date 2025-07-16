from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, condecimal


Money = condecimal(max_digits=20, decimal_places=5)


class UserOut(BaseModel):
    id: int
    user_id: int
    login: Optional[str]
    lang: Optional[str]

    # balances
    balance_ton:      Money = Field(..., example="0.00000")
    balance_payments_ton: Money = Field(..., example="0.00000")
    withdrawal_ton:   Money
    deposit_ton:      Money

    # avatar
    avatar_url_telegram: Optional[str]

    # referral structure
    referrer_id_level1: Optional[int]
    referrer_id_level2: Optional[int]
    referrer_id_level3: Optional[int]
    referral_count_level1: int
    referral_count_level2: int
    referral_count_level3: int
    referral_income_level1: Money
    referral_income_level2: Money
    referral_income_level3: Money

    # cards ‑‑ flat, one field per slot
    card_1: Optional[int]
    time_card_1: Optional[datetime]
    card_1_income: Money

    card_2: Optional[int]
    time_card_2: Optional[datetime]
    card_2_income: Money

    card_3: Optional[int]
    time_card_3: Optional[datetime]
    card_3_income: Money

    card_4: Optional[int]
    time_card_4: Optional[datetime]
    card_4_income: Money

    card_5: Optional[int]
    time_card_5: Optional[datetime]
    card_5_income: Money

    card_6: Optional[int]
    time_card_6: Optional[datetime]
    card_6_income: Money

    card_7: Optional[int]
    time_card_7: Optional[datetime]
    card_7_income: Money

    # misc
    date: datetime
    sub_channel: int = Field(0, example=0)  # Subscription channel status

    class Config:
        orm_mode = True
        json_encoders = {Decimal: lambda v: format(v, "f")}
