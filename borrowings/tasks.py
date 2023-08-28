import asyncio
from celery import shared_task
from aiogram import Bot
import os
from django.utils import timezone
from dotenv import load_dotenv

from borrowings.models import Borrowing
from .telegram_helpers import send_telegram_notification

load_dotenv()


@shared_task
def send_telegram_notification(message):
    send_telegram_notification.delay(message)


@shared_task
def check_overdue_borrowings():
    today = timezone.now().date()
    tomorrow = today + timezone.timedelta(days=1)
    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=tomorrow,
        actual_return_date__isnull=True
    )

    if not overdue_borrowings:
        send_telegram_notification.delay("No borrowings overdue today!")
    else:
        for borrowing in overdue_borrowings:
            message = (
                f"Borrowing overdue: "
                f"User {borrowing.user.email} "
                f"borrowed book '{borrowing.book.title}'. "
                f"Expected return date: {borrowing.expected_return_date}."
            )
            send_telegram_notification.delay(message)

