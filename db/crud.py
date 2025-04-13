from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date
from db.models import (
    MoodEntry,
    HabitEntry,
    HealthEntry,
    WeatherEntry,
    GeomagneticEntry,
    Subscriber
)

async def save_mood(session: AsyncSession, user_id: int, mood: str, comment: str | None = None):
    entry = MoodEntry(user_id=user_id, mood=mood, comment=comment)
    session.add(entry)
    await session.commit()

async def save_habit(session: AsyncSession, user_id: int, habit_name: str, comment: str | None = None):
    entry = HabitEntry(user_id=user_id, habit_name=habit_name, comment=comment)
    session.add(entry)
    await session.commit()

async def save_health(
    session: AsyncSession,
    user_id: int,
    energy_level: int,
    headache: bool,
    sleep_hours: float,
    comment: str | None = None
):
    entry = HealthEntry(
        user_id=user_id,
        energy_level=energy_level,
        headache=headache,
        sleep_hours=sleep_hours,
        comment=comment
    )
    session.add(entry)
    await session.commit()

async def save_weather(session: AsyncSession, date: date, day_type: str, data: dict):
    entry = WeatherEntry(
        date=date,
        type=day_type,
        temperature_avg=data["temperature"]["avg"],
        temperature_min=data["temperature"]["min"],
        temperature_max=data["temperature"]["max"],
        humidity_avg=data["humidity"]["avg"],
        humidity_min=data["humidity"]["min"],
        humidity_max=data["humidity"]["max"],
        pressure_avg=data["pressure"]["avg"],
        pressure_min=data["pressure"]["min"],
        pressure_max=data["pressure"]["max"],
        wind_avg=data["wind"]["avg"],
        wind_min=data["wind"]["min"],
        wind_max=data["wind"]["max"],
        uv_index=data["uv_index"],
        weather_code=data["weather_code"]
    )
    session.add(entry)
    await session.commit()

async def save_geomagnetic(session: AsyncSession, date: date, day_type: str, data: dict):
    entry = GeomagneticEntry(
        date=date,
        type=day_type,
        kp_avg=data["avg"],
        kp_max=data["max"]
    )
    session.add(entry)
    await session.commit()

async def get_weather(session: AsyncSession, date: date, day_type: str):
    stmt = select(WeatherEntry).where(WeatherEntry.date == date, WeatherEntry.type == day_type)
    result = await session.execute(stmt)
    return result.scalars().first()

async def get_geomagnetic(session: AsyncSession, date: date, day_type: str):
    stmt = select(GeomagneticEntry).where(GeomagneticEntry.date == date, GeomagneticEntry.type == day_type)
    result = await session.execute(stmt)
    return result.scalars().first()


async def add_subscriber(session: AsyncSession, chat_id: int, username: str | None):
    exists_stmt = select(Subscriber).where(Subscriber.chat_id == chat_id)
    res = await session.execute(exists_stmt)
    existing = res.scalar_one_or_none()

    if existing:
        existing.active = True
    else:
        session.add(Subscriber(chat_id=chat_id, username=username))

    await session.commit()


async def get_active_subscribers(session: AsyncSession):
    stmt = select(Subscriber).where(Subscriber.active == True)
    res = await session.execute(stmt)
    return res.scalars().all()