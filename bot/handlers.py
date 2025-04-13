from aiogram import Router, types
from aiogram.filters import Command
from bot.keyboards import mood_keyboard
from db.database import get_db
from db import crud
from sqlalchemy.ext.asyncio import async_sessionmaker
from config import BOT_TOKEN

from core.summary import get_today_moods
from ai.analyzer import analyze_day

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я твой AI-ассистент. Готов записывать твоё самочувствие.")


@router.message(Command("mood"))
async def cmd_mood(message: types.Message):
    await message.answer("Выбери своё текущее настроение:", reply_markup=mood_keyboard)

@router.message(lambda msg: msg.text in ["😊", "😐", "😢", "😡", "🤯"])
async def save_mood(message: types.Message):
    async for session in get_db():
        await crud.save_mood(session, message.from_user.id, message.text)
    await message.answer("Записал твоё настроение! 👍", reply_markup=types.ReplyKeyboardRemove())

@router.message(Command("summary"))
async def cmd_summary(message: types.Message):
    async for session in get_db():
        moods = await get_today_moods(session, message.from_user.id)
        mood_list = [m.mood for m in moods]

    if not mood_list:
        await message.answer("У тебя пока нет настроений за сегодня 🙃")
        return

    analysis = await analyze_day(mood_list)
    await message.answer(f"🧠 AI-совет на сегодня:\n\n{analysis}")

def register_handlers(dp):
    dp.include_router(router)
