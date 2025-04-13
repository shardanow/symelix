from sqlalchemy.ext.asyncio import AsyncSession
from db.models import MoodEntry

async def save_mood(session: AsyncSession, user_id: int, mood: str, comment: str | None = None):
    entry = MoodEntry(user_id=user_id, mood=mood, comment=comment)
    session.add(entry)
    await session.commit()
