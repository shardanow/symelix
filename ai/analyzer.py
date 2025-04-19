from openai import AsyncOpenAI
from config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

def format_weather(data: dict) -> str:
    if not data:
        return "Нет данных о погоде."
    
    # Create a safe dictionary access method with defaults
    def safe_get(dictionary, keys, default="Нет данных"):
        """Safely get nested values from a dictionary with a default value if missing"""
        if not dictionary:
            return default
            
        current = dictionary
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current
    
    # Build weather description with safe access to all fields
    weather_parts = []
    
    # Weather code
    weather_code = safe_get(data, ['weather_code'], "Неизвестно")
    weather_parts.append(f"Возможно в течении дня: {weather_code}")
    
    # Temperature
    temp_min = safe_get(data, ['temperature', 'min'], "N/A")
    temp_max = safe_get(data, ['temperature', 'max'], "N/A") 
    temp_avg = safe_get(data, ['temperature', 'avg'], "N/A")
    weather_parts.append(f"Температура: от {temp_min}°C до {temp_max}°C, средняя {temp_avg}°C")
    
    # Pressure
    pressure = safe_get(data, ['pressure', 'avg'], "N/A")
    weather_parts.append(f"Давление: {pressure} гПа")
    
    # Humidity
    humidity = safe_get(data, ['humidity', 'avg'], "N/A")
    weather_parts.append(f"Влажность: {humidity}%")
    
    # Wind
    wind = safe_get(data, ['wind', 'avg'], "N/A")
    weather_parts.append(f"Ветер: {wind} м/с")
    
    # UV Index
    uv_index = safe_get(data, ['uv_index'], "N/A")
    weather_parts.append(f"UV-индекс: {uv_index}")
    
    return ". ".join(weather_parts) + "."

def format_geomagnetic(data: dict | None) -> str:
    if not data or "avg" not in data or "max" not in data:
        return "Нет данных по геомагнитной активности."
    return f"K-индекс геомагнитной активности: средний {data['avg']}, максимум {data['max']}."


async def analyze_day(
    mood_entries: list[dict] | None = None,  # [{"mood": "😊", "comment": "устал"}, ...]
    habit_entries: list[dict] | None = None,  # [{"habit": "💧 Вода", "comment": "выпил только вечером"}, ...]
    health_data: list[dict] | None = None,  # [{"energy_level": 8, "headache": False, "sleep_hours": 7.5, "comment": "всё хорошо"}, ...]
    weather_today: dict | None = None,  # {"temperature": {...}, "humidity": {...}, ...}
    weather_tomorrow: dict | None = None,  # {"temperature": {...}, "humidity": {...}, ...}
    geo_today: dict | None = None,  # {"avg": 3, "max": 5}
    geo_tomorrow: dict | None = None,  # {"avg": 2, "max": 4}
) -> str:
    # Преобразуем эмоции
    moods_text = []
    for m in mood_entries:
        mood_name = m["mood"]
        comment = m["comment"]
        if comment:
            moods_text.append(f"{mood_name} ({comment})")
        else:
            moods_text.append(mood_name)

    # Привычки
    habits_text = []
    for h in habit_entries:
        habit_name = h["habit"]
        comment = h["comment"]
        if comment:
            habits_text.append(f"{habit_name} ({comment})")
        else:
            habits_text.append(habit_name)

    # добавим здоровье:
    health_text = ""
    if health_data:
        h = health_data[-1]  # берём последний, если за день было несколько
        health_text = (
            f"Энергия: {h['energy_level']}/10, "
            f"Сон: {h['sleep_hours']} ч, "
            f"Головная боль: {'да' if h['headache'] else 'нет'}"
        )
        if h["comment"]:
            health_text += f" ({h['comment']})"

   # Погода
    weather_now = format_weather(weather_today)
    weather_next = format_weather(weather_tomorrow)

    # Геомагнитка
    geo_now = format_geomagnetic(geo_today)
    geo_next = format_geomagnetic(geo_tomorrow)


    prompt = (
        f"Ты - профессиональный AI-ассистент по здоровью и благополучию. "
        f"Ты обучен на медицинских исследованиях, нейропсихологии, физиологии сна, влиянии погодных и геомагнитных факторов, "
        f"а также научных данных о привычках и образе жизни.\n\n"

        f"Твоя задача - провести осмысленный анализ состояния пользователя на основе предоставленных данных, "
        f"выявить возможные причины и дать наиболее точные, но доброжелательные рекомендации.\n\n"

        f"Отвечай строго в формате Telegram HTML разметки (используй <b>, <i>, эмодзи и отступы).\n"
        f"Сделай текст структурированным и легко читаемым.\n\n"

        f"🎯 <b>Формат ответа:</b>\n"
        f"🧠 <b>AI-анализ на сегодня</b>\n\n"

        f"💤 <b>Сон:</b> ... (анализ продолжительности, качества, влияния)\n"
        f"😊 <b>Настроение:</b> ... (общий тренд, влияние факторов)\n"
        f"🌦️ <b>Погода:</b> ... (температура, давление, влажность, уровень uv, влияние на самочувствие)\n"
        f"🧲 <b>Геомагнитная активность:</b> ... (уровень K-индекса, влияние на физическое и ментальное состояние)\n\n"

        f"⚠️ <b>Возможные причины самочувствия:</b>\n"
        f"- Научно обоснованные взаимосвязи между всеми факторами (сон + погода + настроение + привычки и т.д.)\n"
        f"- Если всё в норме - так и скажи, это тоже важно\n\n"

        f"💡 <b>Советы на день:</b>\n"
        f"- Короткие, применимые, персонализированные\n"
        f"- Используй научную базу (но без перегруза)\n"
        f"- Дай 3-5 конкретных действия, которые можно применить сегодня\n\n"

        f"📊 <b>Общий вывод:</b>\n"
        f"- Оцени общее состояние: стабильно, средне, тревожно, ресурсно и т.д.\n"
        f"- Поддержи эмоционально. Заверши доброй фразой с эмодзи\n\n"

        f"Вот данные пользователя:\n"
        f"Настроения: {', '.join(moods_text)}\n"
        f"Привычки: {', '.join(habits_text)}\n"
        f"Самочувствие: {health_text}\n\n"
        f"Погода сегодня: {weather_now}\n"
        f"Погода завтра: {weather_next}\n"
        f"Геомагнитная активность сегодня: {geo_now}\n"
        f"Геомагнитная активность завтра: {geo_next}"
    )

    # debug
    print("Prompt:", prompt)


    # Отправляем запрос к GPT-4o-mini
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()