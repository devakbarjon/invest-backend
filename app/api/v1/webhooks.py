from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.database import get_db
from app.models.user import User
from app.models.transaction import Transaction

from app.logging_config import logger

from app.services.bot.bot_base import bot


router = APIRouter(
    prefix="/api/v1/webhooks",
    tags=["Webhooks"]
)


@router.post("/ton-webhook")
async def ton_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    payload = await request.json()
    query_params = dict(request.query_params)

    if query_params.get("secret") != settings.secret_key:
        raise HTTPException(status_code=403, detail="Forbidden")
    

    if payload.get("event") == "incoming_transaction":
        data = payload["data"]
        comment = data.get("comment", "")
        user_id = None
        if comment:
            user_id = int(comment)

            if user_id:
                user = await db.get(User, user_id)

                if user:
                    amount_ton = int(data["amount"]) / 1e9
                    sender = data["from"]
                    tx_hash = data["tx_hash"]

                    user.balance_ton += Decimal(amount_ton)
                    db.add(user)
                    await db.commit()
                    await db.refresh(user)

                    transaction = Transaction(
                        user_id=user.id,
                        amount=Decimal(amount_ton),
                        sender=sender,
                        transaction_type="deposit",
                        transaction_id=tx_hash,
                        status="completed"
                    )
                    db.add(transaction)
                    await db.commit()
                    await db.refresh(transaction)

                    try:

                        await bot.send_message(
                            chat_id=settings.admin_chat_id,
                            text=f"New deposit: {amount_ton} TON from {sender} (User ID: {user_id})"
                        )

                        await bot.send_message(
                            chat_id=user_id,
                            text=f"Your account has been credited with {amount_ton} TON."
                        )

                    except Exception as e:
                        logger.error(f"Failed to send message to user {user_id}: {e}")
                        raise HTTPException(status_code=500, detail="Failed to send notification to user.")


    return {"status": "ok"}