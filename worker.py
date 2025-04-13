import asyncio
from datetime import datetime
from celery import Celery
from aiogram import Bot
from config import TELEGRAM_BOT_TOKEN
from db.database import get_db
from db import crud
from core.summary import get_today_moods, get_today_habits, get_today_health
from ai.analyzer import analyze_day
from celery.schedules import crontab

bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode="HTML")

celery_app = Celery("tasks", broker="redis://redis:6379/0")

@celery_app.task
def send_morning_summary():
    asyncio.run(_send_summary_to_all())


async def _send_summary_to_all():
    async for session in get_db():
        users = await crud.get_active_subscribers(session)
        for user in users:
            await _send_summary(user.chat_id)

async def _send_summary(chat_id: int):
    async for session in get_db():
        moods = await get_today_moods(session, chat_id)
        habits = await get_today_habits(session, chat_id)
        health = await get_today_health(session, chat_id)

        mood_data = [m.to_dict() for m in moods]
        habit_data = [h.to_dict() for h in habits]
        health_data = [h.to_dict() for h in health]

        weather_today = await crud.get_weather(session, datetime.utcnow().date(), "today")
        weather_tomorrow = await crud.get_weather(session, datetime.utcnow().date(), "tomorrow")
        geo_today = await crud.get_geomagnetic(session, datetime.utcnow().date(), "today")
        geo_tomorrow = await crud.get_geomagnetic(session, datetime.utcnow().date(), "tomorrow")

    analysis = await analyze_day(
        mood_entries=mood_data,
        habit_entries=habit_data,
        health_data=health_data,
        weather_today=weather_today.to_dict() if weather_today else {},
        weather_tomorrow=weather_tomorrow.to_dict() if weather_tomorrow else {},
        geo_today=geo_today.to_dict() if geo_today else {},
        geo_tomorrow=geo_tomorrow.to_dict() if geo_tomorrow else {},
    )

    await bot.send_message(chat_id, f"⏰ <b>Утренний совет от AI:</b>\n\n{analysis}")

celery_app.conf.beat_schedule = {
    "send_morning_advice": {
        "task": "worker.send_morning_summary",
        "schedule": crontab(hour=8, minute=0),
    }
}