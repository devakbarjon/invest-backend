from datetime import datetime
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Request

from app.core.config import settings
from app.db.database import get_db


router = APIRouter(
    prefix="/api/v1/webhooks",
    tags=["Webhooks"]
)


@router.post("/ton-webhook")
async def ton_webhook(request: Request):
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
        
        amount_ton = int(data["amount"]) / 1e9
        sender = data["from"]

        print(f"💰 Депозит от UID {user_id}: {amount_ton} TON от {sender}")

        # 🔁 Тут твоя логика зачисления

    return {"status": "ok"}