import openai
from openai import AsyncOpenAI
from config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

emoji_map = {
    "😊": "радость",
    "😐": "нейтральное",
    "😢": "грусть",
    "😡": "злость",
    "🤯": "стресс"
}

async def analyze_day(mood_list: list[str]) -> str:
    text_moods = [emoji_map.get(m, m) for m in mood_list]
    prompt = (
        f"Пользователь сегодня чувствовал: {', '.join(text_moods)}.\n"
        "Сделай короткое, дружелюбное наблюдение и дай совет как улучшить день."
    )

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
