from datetime import datetime, timedelta
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.schemas.users import UserIn, UserOut, UserBuyCardIn, UserBuyCardOut, UserActiveCardOut, UserWithdrawIn, UserWithdrawOut, UserMessage
from app.models.user import User
from app.models.card import Card
from app.models.user_card import UserCard
from app.services.bot.bot_auth import authenticate_user
from app.core.config import settings
from app.logging_config import logger
from app.services.bot.bot_check_sub import check_bot_subscription
from app.services.bot.bot_base import bot

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


@router.post("/withdrawalTon", response_model=UserWithdrawOut)
async def withdrawal_ton(
    user_withdraw_in: UserWithdrawIn,
    db: AsyncSession = Depends(get_db)
):
    user_id = user_withdraw_in.user_id
    amount = user_withdraw_in.amount
    init_data = user_withdraw_in.initData
    wallet_address = user_withdraw_in.wallet

    # Check if the user exists
    user = await authenticate_user(init_data=init_data, user_id=user_id)

    if user.get("success") is False:
        raise HTTPException(status_code=400, detail=user.get("message", "Authentication failed"))
    
    user: User = user.get("user")

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Withdrawal amount must be greater than zero")
    
    if user.balance_payments_ton < Decimal(amount):
        raise HTTPException(status_code=400, detail="Insufficient balance for withdrawal")
    
    try:
        await bot.send_message(
            chat_id=settings.admin_chat_id,
            text=f"Withdrawal request from user {user.user_id} for amount {amount} TON to <code>{wallet_address}</code>.",
            parse_mode="html"
        )
    except Exception as e:
        logger.error(f"Failed to send withdrawal request message: {e}")
        raise HTTPException(status_code=500, detail="Failed to request withdrawal, please try again later.")
    
    # Update user's balance
    user.balance_payments_ton -= Decimal(amount)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return UserWithdrawOut(
        success=1,
        message="Withdrawal request submitted successfully",
        time=datetime.now()
    )


@router.get("/message/user_id={user_id}", response_model=UserMessage)
async def get_referral_message(user_id: int):
    """
    Returns a referral message for sharing.
    """
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    try:   
        inline_query_result = {
            "id": "1",
            "type": "photo",
            "parse_mode": "HTML",
            "caption": "🐸 <b>TonLandia App — Play and Earn TON 💎!</b>\n\n‼️ Join now and start earning TON:",
            "photo_url": "https://www.api-nodeland.com/refimg.jpg",
            "thumbnail_url": "https://www.api-nodeland.com/refimg.jpg",
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {
                            "text": "🐸 Play And Meme",
                            "url": f"https://t.me/TONlandiaBot/game?startapp={user_id}"
                        }
                    ]
                ]
            }
    }

        prepared_inline_message = await bot.save_prepared_inline_message(
            user_id,
            inline_query_result,
            allow_user_chats=True,
            allow_bot_chats=False,
            allow_group_chats=True,
            allow_channel_chats=False
        )

        return UserMessage(
            status=1,
            message="Referral message prepared successfully",
            id=prepared_inline_message.id,
            expiration_date=prepared_inline_message.expiration_date
        )
    
    except Exception as e:
        logger.error(f"Failed to send referral message: {e}")
        raise HTTPException(status_code=500, detail="Failed to send referral message, please try again later.")