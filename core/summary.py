from sqlalchemy import select
from datetime import datetime, timedelta
from db.models import MoodEntry

async def get_today_moods(session, user_id: int):
    now = datetime.utcnow()
    today_start = datetime(now.year, now.month, now.day)
    stmt = select(MoodEntry).where(
        MoodEntry.user_id == user_id,
        MoodEntry.timestamp >= today_start
    )
    result = await session.execute(stmt)
    return result.scalars().all()
