import asyncio
from datetime import datetime, timedelta, date

from integrations.weather import get_weather_forecast
from integrations.geomagnetic import get_geomagnetic_activity
from db.database import get_db
from db import crud
from config import LATITUDE, LONGITUDE

# get coordinates from config
LAT = float(LATITUDE) if LATITUDE else 50.450001 # Default to Kiev
LON = float(LONGITUDE) if LONGITUDE else 30.523333  # Default to Kiev

async def update_external_data():
    today = datetime.utcnow().date()
    tomorrow = today + timedelta(days=1)

    weather = await get_weather_forecast(LAT, LON)
    geomagnetic = await get_geomagnetic_activity()

    async for session in get_db():
        # Weather data
        await crud.save_weather(session, today, "today", weather["today"])
        await crud.save_weather(session, tomorrow, "tomorrow", weather["tomorrow"])

        # Geomagnetic activity data
        if geomagnetic["today"]["avg"] is not None:
            await crud.save_geomagnetic(session, today, "today", geomagnetic["today"])
        if geomagnetic["tomorrow"]["avg"] is not None:
            await crud.save_geomagnetic(session, tomorrow, "tomorrow", geomagnetic["tomorrow"])

    print("✅ Data was recieved and saved.")

if __name__ == "__main__":
    asyncio.run(update_external_data())
