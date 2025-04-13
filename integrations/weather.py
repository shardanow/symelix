import aiohttp
from datetime import datetime, timedelta

BASE_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "☀️ Ясно",
    1: "🌤️ Частично облачно",
    2: "⛅ Переменная облачность",
    3: "☁️ Пасмурно",
    45: "🌫️ Туман",
    48: "🌫️ Туман с инеем",
    51: "🌦️ Слабая морось",
    61: "🌧️ Лёгкий дождь",
    63: "🌧 Умеренный дождь",
    65: "🌧️ Сильный дождь",
    71: "🌨️ Лёгкий снег",
    73: "🌨 Умеренный снег",
    75: "❄️ Сильный снег",
    95: "⛈️ Гроза",
    99: "⛈️ Гроза с градом"
}

def aggregate_weather_day(values: list[float]) -> dict:
    if not values:
        return {"avg": None, "min": None, "max": None}
    return {
        "avg": round(sum(values) / len(values), 2),
        "min": round(min(values), 2),
        "max": round(max(values), 2)
    }

async def get_weather_forecast(lat: float, lon: float) -> dict:
    now = datetime.utcnow()
    today = now.date()
    tomorrow = today + timedelta(days=1)

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,pressure_msl,windspeed_10m",
        "daily": "uv_index_max,weathercode",
        "timezone": "auto"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, params=params) as response:
            if response.status != 200:
                raise Exception(f"Weather API error: {response.status}")
            data = await response.json()

    hourly = data["hourly"]
    daily = data["daily"]

    result = {
        "today": {
            "temperature": [],
            "humidity": [],
            "pressure": [],
            "wind": [],
            "uv_index": None,
            "weather_code": None
        },
        "tomorrow": {
            "temperature": [],
            "humidity": [],
            "pressure": [],
            "wind": [],
            "uv_index": None,
            "weather_code": None
        }
    }

    for i, timestamp in enumerate(hourly["time"]):
        ts = datetime.fromisoformat(timestamp)
        date_key = "today" if ts.date() == today else "tomorrow" if ts.date() == tomorrow else None
        if date_key:
            result[date_key]["temperature"].append(hourly["temperature_2m"][i])
            result[date_key]["humidity"].append(hourly["relative_humidity_2m"][i])
            result[date_key]["pressure"].append(hourly["pressure_msl"][i])
            result[date_key]["wind"].append(hourly["windspeed_10m"][i])

    for i, date_str in enumerate(daily["time"]):
        if date_str == str(today):
            result["today"]["uv_index"] = daily["uv_index_max"][i]
            result["today"]["weather_code"] = WEATHER_CODES.get(daily["weathercode"][i], "неизвестно")
        elif date_str == str(tomorrow):
            result["tomorrow"]["uv_index"] = daily["uv_index_max"][i]
            result["tomorrow"]["weather_code"] = WEATHER_CODES.get(daily["weathercode"][i], "неизвестно")

    aggregated = {
        "today": {
            "temperature": aggregate_weather_day(result["today"]["temperature"]),
            "humidity": aggregate_weather_day(result["today"]["humidity"]),
            "pressure": aggregate_weather_day(result["today"]["pressure"]),
            "wind": aggregate_weather_day(result["today"]["wind"]),
            "uv_index": result["today"]["uv_index"],
            "weather_code": result["today"]["weather_code"]
        },
        "tomorrow": {
            "temperature": aggregate_weather_day(result["tomorrow"]["temperature"]),
            "humidity": aggregate_weather_day(result["tomorrow"]["humidity"]),
            "pressure": aggregate_weather_day(result["tomorrow"]["pressure"]),
            "wind": aggregate_weather_day(result["tomorrow"]["wind"]),
            "uv_index": result["tomorrow"]["uv_index"],
            "weather_code": result["tomorrow"]["weather_code"]
        }
    }

    return aggregated
