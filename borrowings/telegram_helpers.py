import asyncio
import os

from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv

load_dotenv()

BOT = Bot(token=os.environ.get("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher(BOT)


@dp.message_handler(commands=["id"])
async def get_chat_id(message: types.Message):
    await message.answer(text=message.from_user.id)


async def send_telegram_notification(message):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)


async def main():
    message = "Hello, this is a test notification!"
    await send_telegram_notification(message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
