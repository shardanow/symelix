import asyncio
import nest_asyncio
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import TELEGRAM_BOT_TOKEN
from db.database import get_db
from db import crud
from tasks.celery_app import celery_app

# Loop for running async tasks in a synchronous context
# This is necessary for running async tasks in a synchronous context
# such as Celery tasks, which are typically run in a synchronous context.
# This is a workaround for the issue of running async tasks in a synchronous context
nest_asyncio.apply()


@celery_app.task
def remind_hydrate():
    print("🔥 Задача remind_hydrate запущена")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_run_reminder("💧 Напоминание: не забудь выпить воды!"))


@celery_app.task
def remind_vitamins():
    print("💊 Задача remind_vitamins запущена")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_run_reminder("💊 Напоминание: не забудь выпить витамины!"))


async def _run_reminder(message_text: str):
    bot = Bot(
        token=TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True,
            protect_content=False
        )
    )

    try:
        async for session in get_db():
            users = await crud.get_active_subscribers(session)
            for user in users:
                await bot.send_message(user.chat_id, message_text)
    finally:
        await bot.session.close()
