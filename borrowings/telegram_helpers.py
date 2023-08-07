import asyncio
import os

from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()


async def send_telegram_notification(message):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)


async def main():
    message = "Hello, this is a test notification!"
    await send_telegram_notification(message)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
