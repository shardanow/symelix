import asyncio
from datetime import datetime
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import TELEGRAM_BOT_TOKEN
from db.database import get_db
from db import crud
from core.summary import get_today_moods, get_today_habits, get_today_health
from ai.analyzer import analyze_day

# Using DefaultBotProperties for setting default properties
bot = Bot(
    token=TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
        link_preview_is_disabled=True,
        protect_content=False
    )
)

async def get_active_users():
    """Get all active subscribers using a dedicated async context"""
    async for session in get_db():
        return await crud.get_active_subscribers(session)

async def send_summary(chat_id: int):
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

    await bot.send_message(chat_id, f"\u23F0 <b>Утренний совет от AI:</b>\n\n{analysis}")

async def send_summary_to_all():
    async for session in get_db():
        users = await crud.get_active_subscribers(session)
        for user in users:
            await send_summary(user.chat_id)