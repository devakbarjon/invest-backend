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
    balance_ton:      Money = Field(..., example="0.0000")
    balance_payments_ton: Money = Field(..., example="0.0000")
    withdrawal_ton:   Money = Field(..., example="0.0000")
    deposit_ton:      Money = Field(..., example="0.0000")

    # avatar
    avatar_url_telegram: Optional[str]

    # referral structure
    referrer_id_level1: Optional[int]
    referrer_id_level2: Optional[int]
    referrer_id_level3: Optional[int]
    referral_count_level1: int
    referral_count_level2: int
    referral_count_level3: int
    referral_income_level1: Money = Field(..., example="0.0000")
    referral_income_level2: Money = Field(..., example="0.0000")
    referral_income_level3: Money = Field(..., example="0.0000")

    # cards ‑‑ flat, one field per slot
    card_1: Optional[int]
    time_card_1: Optional[datetime]
    card_1_income: Money = Field(..., example="0.0000")

    card_2: Optional[int]
    time_card_2: Optional[datetime]
    card_2_income: Money = Field(..., example="0.0000")

    card_3: Optional[int]
    time_card_3: Optional[datetime]
    card_3_income: Money = Field(..., example="0.0000")

    card_4: Optional[int]
    time_card_4: Optional[datetime]
    card_4_income: Money = Field(..., example="0.0000")

    card_5: Optional[int]
    time_card_5: Optional[datetime]
    card_5_income: Money = Field(..., example="0.0000")

    card_6: Optional[int]
    time_card_6: Optional[datetime]
    card_6_income: Money = Field(..., example="0.0000")

    card_7: Optional[int]
    time_card_7: Optional[datetime]
    card_7_income: Money = Field(..., example="0.0000")

    # misc
    date: datetime
    sub_channel: int = Field(0, example=0)

    class Config:
        orm_mode = True
        json_encoders = {
            Decimal: lambda v: format(v, "f"),
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }


class UserIn(BaseModel):
    user_id: int
    initData: str
    start_param: str | int | None = 0


class UserBuyCardIn(BaseModel):
    user_id: int
    card_id: int
    initData: str

class UserBuyCardOut(BaseModel):
    success: int = Field(1, example=1)
    message: str = Field("Card purchased successfully", example="Card purchased successfully")
    time: datetime
    new_time: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }


class UserActiveCardOut(BaseModel):
    success: int = Field(1, example=1)
    message: str = Field("Card activated successfully", example="Card activated successfully")
    time: datetime
    new_time: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }