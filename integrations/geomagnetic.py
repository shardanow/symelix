import aiohttp
from datetime import datetime, timedelta

NOAA_URL = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"

def aggregate_k_index(values: list[float]) -> dict:
    if not values:
        return {"avg": None, "max": None}
    return {
        "avg": round(sum(values) / len(values), 2),
        "max": round(max(values), 2)
    }

async def get_geomagnetic_activity() -> dict:
    now = datetime.utcnow()
    today = now.date()
    tomorrow = today + timedelta(days=1)

    async with aiohttp.ClientSession() as session:
        async with session.get(NOAA_URL) as response:
            if response.status != 200:
                raise Exception(f"K-index API error: {response.status}")
            data = await response.json()

    result = {
        "today": [],
        "tomorrow": []
    }

    for entry in data:
        time_str = entry.get("time_tag")
        kp = entry.get("kp_index")
        if time_str and kp is not None:
            ts = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
            if ts.date() == today:
                result["today"].append(kp)
            elif ts.date() == tomorrow:
                result["tomorrow"].append(kp)

    return {
        "today": aggregate_k_index(result["today"]),
        "tomorrow": aggregate_k_index(result["tomorrow"])
    }
