import sys
import os
import json
from urllib.parse import parse_qsl
from datetime import datetime, timedelta

from aiogram.utils.web_app import check_webapp_signature
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.core.config import settings
from app.db.database import get_db

async def authenticate_user(init_data: str, user_id: str | int, start_param: str | int | None=0) -> dict:
    """
    Authenticates a user using Telegram Web App initData.
    
    Args:
        init_data (str): The initData string from the Telegram Web App.
        start_param (str | int | None): Optional start parameter from the bot.
    
    Returns:
        dict: User information if authentication is successful, None otherwise.
    """
    # Validate the initData
    def validate_init_data(init_data: str) -> bool:
        status = check_webapp_signature(settings.bot_token, init_data)
        return status

    if not validate_init_data(init_data):
        return {"success": False, "message": "Invalid initData!"}

    # Parse the initData
    data_dict = dict(parse_qsl(init_data))
    
    # Check if auth_date is recent (within 24 hours)
    # auth_date = int(data_dict.get("auth_date", 0))
    # if datetime.now() - datetime.fromtimestamp(auth_date) > timedelta(hours=24):
    #     return {"success": False, "message": "auth_date is too old!"}
    
    user_data = data_dict.get("user")
    if not user_data:
        return {"success": False, "message": "No user data found!"}

    user = json.loads(user_data)
    user_data_id = user.get("id")
    photo_url = user.get("photo_url")
    username = user.get("username")
    lang_code = user.get("language_code", "en")

    if user_id != user_data_id:
        return {"success": False, "message": "User ID mismatch!"}

    # Authenticate the user (or create a new account)
    async def user_exists_in_database(user_id: int) -> User:
        async for db in get_db():
            result = await db.execute(
                select(User)
                .options(selectinload(User.user_cards))
                .where(User.user_id == user_id)
            )
            user = result.scalars().first()
            if not user:
                user = User(
                    user_id=user_id,
                    avatar_url_telegram=photo_url,
                    referrer_id_level1=start_param if isinstance(start_param, int) else None,
                    login=username,
                    lang=lang_code,
                )
                db.add(user)
                await db.commit()
                await db.refresh(user)
            return user
    
    user = await user_exists_in_database(user_id)

    return {
        "success": True,
        "user": user
        }