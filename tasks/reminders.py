import asyncio
from aiogram import Bot
from config import TELEGRAM_BOT_TOKEN
from db.database import get_db
from db import crud
from .celery_app import celery_app

bot = Bot(token=TELEGRAM_BOT_TOKEN)

@celery_app.task
def remind_hydrate():
    asyncio.run(_send_reminder_hydrate_to_all())

async def _send_reminder_hydrate_to_all():
    async for session in get_db():
        users = await crud.get_active_subscribers(session)
        for user in users:
            await bot.send_message(user.chat_id, "💧 Напоминание: не забудь выпить воды!")

@celery_app.task
def remind_vitamins():
    asyncio.run(_send_reminder_vitamins_to_all())

async def _send_reminder_vitamins_to_all():
    async for session in get_db():
        users = await crud.get_active_subscribers(session)
        for user in users:
            await bot.send_message(user.chat_id, "💊 Напоминание: не забудь выпить витамины!")
