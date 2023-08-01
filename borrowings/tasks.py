import asyncio

from celery import shared_task
from aiogram import Bot
import os
import logging

from django.utils import timezone
from dotenv import load_dotenv

from borrowings.models import Borrowing

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
def check_overdue_borrowings():
    today = timezone.now().date()
    tomorrow = today + timezone.timedelta(days=1)
    overdue_borrowings = Borrowing.objects.filter(expected_return_date__lte=tomorrow, actual_return_date__isnull=True)

    if not overdue_borrowings:
        send_telegram_notification.delay("No borrowings overdue today!")
    else:
        for borrowing in overdue_borrowings:
            message = (
                f"Borrowing overdue: "
                f"User {borrowing.user.email} borrowed book '{borrowing.book.title}'. "
                f"Expected return date: {borrowing.expected_return_date}."
            )
            send_telegram_notification.delay(message)


@shared_task
def say_hello():
    logger.info("Hello, world!")
    return "Hello, world!"
