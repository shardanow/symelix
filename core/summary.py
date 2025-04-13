from sqlalchemy import select
from datetime import datetime
from db.models import MoodEntry, HabitEntry, HealthEntry

async def get_today_moods(session, user_id: int):
    now = datetime.utcnow()
    start = datetime(now.year, now.month, now.day)
    stmt = select(MoodEntry).where(
        MoodEntry.user_id == user_id,
        MoodEntry.timestamp >= start
    )
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_today_habits(session, user_id: int):
    now = datetime.utcnow()
    start = datetime(now.year, now.month, now.day)
    stmt = select(HabitEntry).where(
        HabitEntry.user_id == user_id,
        HabitEntry.timestamp >= start
    )
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_today_health(session, user_id: int):
    now = datetime.utcnow()
    start = datetime(now.year, now.month, now.day)
    stmt = select(HealthEntry).where(
        HealthEntry.user_id == user_id,
        HealthEntry.timestamp >= start
    )
    result = await session.execute(stmt)
    return result.scalars().all()
