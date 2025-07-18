from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.schemas.users import UserIn, UserOut, UserBuyCardIn, UserBuyCardOut, UserActiveCardOut
from app.models.user import User
from app.models.card import Card
from app.models.user_card import UserCard
from app.services.bot.bot_auth import authenticate_user
from app.core.config import settings

from app.logging_config import logger
from app.services.bot.bot_check_sub import check_bot_subscription

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)


@router.post("/getUser", response_model=UserOut)
async def get_user(
    user_in: UserIn,
    db: AsyncSession = Depends(get_db)
):
    user_id = user_in.user_id
    init_data = user_in.initData
    start_param = user_in.start_param
    
    user_data = {}
    user = await authenticate_user(
        init_data=init_data,
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
    user_data["date"] = datetime.now()
    user_data["sub_channel"] = await check_bot_subscription(user_id, settings.bot_channel_id)

    return UserOut.model_validate(user_data)


@router.post("/buyCard", response_model=UserBuyCardOut)
async def buy_card(
    user_buy_card_in: UserBuyCardIn,
    db: AsyncSession = Depends(get_db)
):
    user_id = user_buy_card_in.user_id
    card_id = user_buy_card_in.card_id
    init_data = user_buy_card_in.initData

    # Check if the user exists
    user = await authenticate_user(init_data=init_data, user_id=user_id)

    if user.get("success") is False:
        raise HTTPException(status_code=400, detail=user.get("message", "Authentication failed"))
    
    user: User = user.get("user")

    # Check if the card exists
    card: Card = await db.get(Card, card_id)

    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    result = await db.execute(
        select(UserCard).where(UserCard.user_id == user.id, UserCard.card_id == card.id, UserCard.status == True)
    )
    user_card = result.scalars().first()

    if user_card:
        raise HTTPException(status_code=400, detail="Card already purchased")
    
    if user.balance_ton < card.cost:
        raise HTTPException(status_code=400, detail="Insufficient balance to buy the card")
    
    # Update user's balance
    user.balance_ton -= card.cost
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Create a new UserCard
    user_card = UserCard(
        user_id=user.user_id,
        card_id=card.id,
        next_cycle=datetime.now() + timedelta(hours=card.cycle_time),
        status=True
    )
    db.add(user_card)
    await db.commit()
    await db.refresh(user_card)

    return UserBuyCardOut(
        success=1,
        message="Card purchased successfully",
        time=datetime.now(),
        new_time= user_card.next_cycle
    )


@router.post("/activeCard", response_model=UserActiveCardOut)
async def active_card(
    user_active_card_in: UserBuyCardIn,
    db: AsyncSession = Depends(get_db)
):
    user_id = user_active_card_in.user_id
    card_id = user_active_card_in.card_id
    init_data = user_active_card_in.initData

    # Check if the user exists
    user = await authenticate_user(init_data=init_data, user_id=user_id)

    if user.get("success") is False:
        raise HTTPException(status_code=400, detail=user.get("message", "Authentication failed"))
    
    user: User = user.get("user")

    # Check if the card exists
    card: Card = await db.get(Card, card_id)

    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    result = await db.execute(
        select(UserCard).where(UserCard.user_id == user.id, UserCard.card_id == card.id, UserCard.status == True)
    )
    user_card = result.scalars().first()

    if not user_card:
        raise HTTPException(status_code=404, detail="User does not own this card")
    
    # Activate the card
    user_card.next_cycle = datetime.now() + timedelta(hours=card.cycle_time)
    db.add(user_card)
    await db.commit()
    await db.refresh(user_card)

    return UserActiveCardOut(
        success=1,
        message="Card activated successfully",
        time=datetime.now(),
        new_time=user_card.next_cycle
    )