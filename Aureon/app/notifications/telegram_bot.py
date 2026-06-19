"""
Telegram Bot Notification Module.
Sends real-time logs and trading alerts asynchronously via the Telegram Bot API.
"""

import httpx
from typing import Optional
from app.utils.config import settings
from app.utils.logger import app_logger


async def send_telegram_message(message: str) -> bool:
    """
    Asynchronously posts a message to the configured Telegram chat.
    
    Args:
        message: Plain text or markdown formatted string.
        
    Returns:
        bool: True if sent successfully, False otherwise.
    """
    if not settings.TELEGRAM_ENABLED:
        app_logger.debug("Telegram notifications are disabled in settings.")
        return False

    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        app_logger.warning("Telegram enabled but credentials (TOKEN/CHAT_ID) are missing.")
        return False

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                app_logger.info("Telegram notification sent successfully.")
                return True
            else:
                app_logger.error(f"Telegram API returned non-200 code: {response.status_code} - {response.text}")
                return False
    except Exception as e:
        app_logger.error(f"Failed to transmit Telegram notification: {e}")
        return False
