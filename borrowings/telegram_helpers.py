import asyncio
from aiogram import Bot


async def send_telegram_notification(message):
    bot_token = "6155357404:AAG_oKggBJTFzJsOPokvQ1SwU5eqWMh34gk"
    chat_id = 382864435

    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)


async def main():
    message = "Hello, this is a test notification!"
    await send_telegram_notification(message)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
