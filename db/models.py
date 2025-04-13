from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class MoodEntry(Base):
    __tablename__ = "mood_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    mood: Mapped[str]
    comment: Mapped[str | None]
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
