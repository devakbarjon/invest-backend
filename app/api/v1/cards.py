from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.card import Card
from app.models.schemas.cards import CardOut, CardIn
from app.services.bot.bot_auth import authenticate_user
from app.logging_config import logger


router = APIRouter(
    prefix="/api/v1/cards",
    tags=["Cards"]
)


@router.post("/", response_model=list[CardOut])
async def get_all_cards(
    card_in: CardIn,
    db: AsyncSession = Depends(get_db)
):
    """
    Returns all available cards.
    """
    init_data = card_in.initData
    user_id = card_in.user_id

    user = await authenticate_user(
        init_data=init_data,
        start_param=0,
        user_id=user_id
    )

    if user.get("success") is False:
        raise HTTPException(status_code=400, detail=user.get("message", "Authentication failed"))
    
    user = user.get("user")

    result = await db.execute(select(Card))
    cards: list[Card] = result.scalars().all()
    
    if not cards:
        raise HTTPException(status_code=404, detail="No cards found")
    
    return [CardOut.model_validate(card, from_attributes=True) for card in cards]