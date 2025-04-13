from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, date

class Base(DeclarativeBase):
    pass

class MoodEntry(Base):
    __tablename__ = "mood_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    mood: Mapped[str]
    comment: Mapped[str | None]
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)

class HabitEntry(Base):
    __tablename__ = "habit_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    habit_name: Mapped[str]
    comment: Mapped[str | None]
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)

class HealthEntry(Base):
    __tablename__ = "health_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    energy_level: Mapped[int]  # от 1 до 10
    headache: Mapped[bool]
    sleep_hours: Mapped[float]
    comment: Mapped[str | None]
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class WeatherEntry(Base):
    __tablename__ = "weather_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date]
    type: Mapped[str]  # "today" or "tomorrow"
    temperature_avg: Mapped[float]
    temperature_min: Mapped[float]
    temperature_max: Mapped[float]
    humidity_avg: Mapped[float]
    humidity_min: Mapped[float]
    humidity_max: Mapped[float]
    pressure_avg: Mapped[float]
    pressure_min: Mapped[float]
    pressure_max: Mapped[float]
    wind_avg: Mapped[float]
    wind_min: Mapped[float]
    wind_max: Mapped[float]
    uv_index: Mapped[float]
    weather_code: Mapped[str]
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def to_dict(self):
        return {
            "temperature": {
                "avg": self.temperature_avg,
                "min": self.temperature_min,
                "max": self.temperature_max
            },
            "humidity": {
                "avg": self.humidity_avg,
                "min": self.humidity_min,
                "max": self.humidity_max
            },
            "pressure": {
                "avg": self.pressure_avg,
                "min": self.pressure_min,
                "max": self.pressure_max
            },
            "wind": {
                "avg": self.wind_avg,
                "min": self.wind_min,
                "max": self.wind_max
            },
            "uv_index": self.uv_index,
            "weather_code": self.weather_code
        }


class GeomagneticEntry(Base):
    __tablename__ = "geomagnetic_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date]
    type: Mapped[str]  # "today" or "tomorrow"
    kp_avg: Mapped[float]
    kp_max: Mapped[float]
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def to_dict(self):
        return {
            "avg": self.kp_avg,
            "max": self.kp_max
        }
