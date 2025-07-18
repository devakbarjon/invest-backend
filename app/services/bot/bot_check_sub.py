from app.logging_config import logger
from .bot_base import bot


async def check_bot_subscription(user_id: int, channel_id: int) -> int:
    """
    Check if the user is subscribed to the bot's channel.
    
    Args:
        user_id (int): The Telegram user ID.
        channel_id (int): The Telegram channel ID to check subscription against.
    
    Returns:
        int: 0 if the user is subscribed, 0 otherwise.
    """
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            return 0
        return 1
    except Exception as e:
        logger.error(f"Error checking subscription for user {user_id}: {e}")
        return 1