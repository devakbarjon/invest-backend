from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.schemas.users import UserOut
from app.models.user import User
from app.models.card import Card
from app.models.user_card import UserCard
from app.services.bot.bot_auth import authenticate_user

from app.logging_config import logger

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)


@router.get("/", response_model=UserOut)
async def get_user(
    user_id: int,
    initData: str,
    start_param: str | int | None = 0,
    db: AsyncSession = Depends(get_db)
):
    """
    Return user details by user_id.
    """
    user_data = {}
    user = await authenticate_user(
        init_data=initData,
        start_param=start_param,
        user_id=user_id
    )

    if user.get("success") is False:
        raise HTTPException(status_code=400, detail=user.get("message", "Authentication failed"))
    
    user: User = user.get("user")
    all_cards = (await db.scalars(select(Card))).all()
    user_cards = (await db.scalars(select(UserCard).where(UserCard.user_id == user.id))).all()

    for card in all_cards:
        user_data[f"card_{card.id}"] = 0
        user_data[f"time_card_{card.id}"] = None
        user_data[f"card_{card.id}_income"] = "0.0000"
        
    for ucard in user_cards:
        if ucard.status:
            user_data["card_{ucard.id}"] = 1
            user_data["time_card_{ucard.id}"]  = ucard.next_cycle.isoformat()
            user_data["card_{ucard.id}_income"] = str(ucard.income)

    user_data["id"] = user.id
    user_data["user_id"] = user.user_id
    user_data["login"] = user.login
    user_data["lang"] = user.lang
    user_data["avatar_url_telegram"] = user.avatar_url_telegram
    user_data["balance_ton"] = str(user.balance_ton)
    user_data["balance_payments_ton"] = str(user.balance_payments_ton)
    user_data["referrer_id_level1"] = user.referrer_id_level1
    user_data["referrer_id_level2"] = user.referrer_id_level2
    user_data["referrer_id_level3"] = user.referrer_id_level3
    user_data["referral_count_level1"] = user.referral_count_level1
    user_data["referral_count_level2"] = user.referral_count_level2
    user_data["referral_count_level3"] = user.referral_count_level3
    user_data["referral_income_level1"] = str(user.referral_income_level1)
    user_data["referral_income_level2"] = str(user.referral_income_level2)
    user_data["referral_income_level3"] = str(user.referral_income_level3)
    user_data["withdrawal_ton"] = str(user.withdrawal_ton)
    user_data["deposit_ton"] = str(user.deposit_ton)
    user_data["date"] = datetime.now().isoformat()
    user_data["sub_channel"] = 0

    return UserOut.model_validate(user_data)