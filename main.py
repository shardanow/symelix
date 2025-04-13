import asyncio
from aiogram import Bot, Dispatcher
from bot.handlers import register_handlers
from config import BOT_TOKEN

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    register_handlers(dp)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
