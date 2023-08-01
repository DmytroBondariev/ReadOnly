import asyncio

from celery import shared_task
from aiogram import Bot
import os
import logging

from dotenv import load_dotenv


logger = logging.getLogger(__name__)
load_dotenv()


@shared_task
def send_telegram_notification(message):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    bot = Bot(token=bot_token)

    async def send_notification():
        await bot.send_message(chat_id=chat_id, text=message)

    """Running the async function in the event loop"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_notification())


@shared_task
def say_hello():
    logger.info("Hello, world!")
    return "Hello, world!"
