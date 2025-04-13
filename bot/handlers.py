from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from bot.keyboards import (
    mood_keyboard,
    habit_keyboard,
    yes_no_keyboard,
    energy_keyboard,
    headache_keyboard
)
from db.database import get_db
from db import crud
from config import TELEGRAM_BOT_TOKEN

from core.summary import get_today_moods, get_today_habits, get_today_health
from ai.analyzer import analyze_day
from datetime import datetime, timedelta


router = Router()


# === Состояния для FSM ===
class MoodStates(StatesGroup):
    ask_comment = State()
    waiting_for_comment = State()

class HabitStates(StatesGroup):
    ask_comment = State()
    waiting_for_comment = State()

class HealthStates(StatesGroup):
    waiting_for_energy = State()
    waiting_for_sleep = State()
    waiting_for_headache = State()
    ask_comment = State()
    waiting_for_comment = State()



# === Старт ===
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я твой AI-ассистент. Готов записывать твоё самочувствие.")


# === Настроение ===
@router.message(Command("mood"))
async def cmd_mood(message: types.Message):
    await message.answer("Выбери своё текущее настроение:", reply_markup=mood_keyboard)

@router.message(lambda msg: any(x in msg.text for x in ["😊", "😐", "😢", "😡", "🤯"]))
async def mood_chosen(message: types.Message, state: FSMContext):
    await state.update_data(mood=message.text)
    await message.answer("Хочешь добавить комментарий к настроению?", reply_markup=yes_no_keyboard)
    await state.set_state(MoodStates.ask_comment)

@router.message(MoodStates.ask_comment)
async def mood_comment_decision(message: types.Message, state: FSMContext):
    if message.text.lower() == "нет":
        data = await state.get_data()
        async for session in get_db():
            await crud.save_mood(session, message.from_user.id, data["mood"], None)
        await message.answer("Записал твоё настроение! 👍", reply_markup=ReplyKeyboardRemove())
        await state.clear()
    elif message.text.lower() == "да":
        await message.answer("Хорошо, напиши комментарий:")
        await state.set_state(MoodStates.waiting_for_comment)
    else:
        await message.answer("Пожалуйста, выбери 'Да' или 'Нет'.")

@router.message(MoodStates.waiting_for_comment)
async def mood_comment(message: types.Message, state: FSMContext):
    data = await state.get_data()
    comment = message.text.strip()

    async for session in get_db():
        await crud.save_mood(session, message.from_user.id, data["mood"], comment)

    await message.answer("Записал твоё настроение с комментарием! 📝", reply_markup=ReplyKeyboardRemove())
    await state.clear()


# === Привычка ===
@router.message(Command("habit"))
async def cmd_habit(message: types.Message):
    await message.answer("Отметь выполненную привычку:", reply_markup=habit_keyboard)

@router.message(lambda msg: any(x in msg.text for x in ["💧", "💊", "🚶‍♂️", "🧘"]))
async def habit_chosen(message: types.Message, state: FSMContext):
    await state.update_data(habit=message.text.strip())
    await message.answer("Хочешь добавить комментарий к привычке?", reply_markup=yes_no_keyboard)
    await state.set_state(HabitStates.ask_comment)

@router.message(HabitStates.ask_comment)
async def habit_comment_decision(message: types.Message, state: FSMContext):
    if message.text.lower() == "нет":
        data = await state.get_data()
        async for session in get_db():
            await crud.save_habit(session, message.from_user.id, data["habit"], None)
        await message.answer("Привычка сохранена 💪", reply_markup=ReplyKeyboardRemove())
        await state.clear()
    elif message.text.lower() == "да":
        await message.answer("Хорошо, напиши комментарий:")
        await state.set_state(HabitStates.waiting_for_comment)
    else:
        await message.answer("Пожалуйста, выбери 'Да' или 'Нет'.")

@router.message(HabitStates.waiting_for_comment)
async def habit_comment(message: types.Message, state: FSMContext):
    data = await state.get_data()
    comment = message.text.strip()

    async for session in get_db():
        await crud.save_habit(session, message.from_user.id, data["habit"], comment)

    await message.answer("Привычка сохранена с комментарием 💬", reply_markup=ReplyKeyboardRemove())
    await state.clear()

# === Команда /health ===
@router.message(Command("health"))
async def cmd_health(message: types.Message, state: FSMContext):
    await message.answer("На сколько ты оцениваешь свою энергию от 1 до 10?", reply_markup=energy_keyboard)
    await state.set_state(HealthStates.waiting_for_energy)

@router.message(HealthStates.waiting_for_energy)
async def set_energy(message: types.Message, state: FSMContext):
    try:
        energy = int(message.text)
        if not (1 <= energy <= 10):
            raise ValueError
        await state.update_data(energy_level=energy)
        await message.answer("Сколько часов ты спал(а) прошлой ночью? (например: 6.5)")
        await state.set_state(HealthStates.waiting_for_sleep)
    except ValueError:
        await message.answer("Пожалуйста, выбери число от 1 до 10 из кнопок.")

@router.message(HealthStates.waiting_for_sleep)
async def set_sleep(message: types.Message, state: FSMContext):
    try:
        hours = float(message.text)
        await state.update_data(sleep_hours=hours)
        await message.answer("Была ли у тебя головная боль сегодня?", reply_markup=headache_keyboard)
        await state.set_state(HealthStates.waiting_for_headache)
    except ValueError:
        await message.answer("Пожалуйста, введи количество часов сна, например: 7.5")

@router.message(HealthStates.waiting_for_headache)
async def set_headache(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    if answer not in ["да", "нет"]:
        await message.answer("Пожалуйста, выбери Да или Нет.")
        return

    headache = answer == "да"
    await state.update_data(headache=headache)
    await message.answer("Хочешь добавить комментарий к самочувствию?", reply_markup=yes_no_keyboard)
    await state.set_state(HealthStates.ask_comment)


@router.message(HealthStates.ask_comment)
async def handle_comment_decision(message: types.Message, state: FSMContext):
    if message.text.lower() == "нет":
        data = await state.get_data()
        async for session in get_db():
            await crud.save_health(
                session=session,
                user_id=message.from_user.id,
                energy_level=data["energy_level"],
                headache=data["headache"],
                sleep_hours=data["sleep_hours"],
                comment=None
            )
        await message.answer("Спасибо! Записал твоё самочувствие 🩺", reply_markup=ReplyKeyboardRemove())
        await state.clear()
    elif message.text.lower() == "да":
        await message.answer("Хорошо, напиши комментарий:")
        await state.set_state(HealthStates.waiting_for_comment)
    else:
        await message.answer("Пожалуйста, выбери 'Да' или 'Нет'.")


@router.message(HealthStates.waiting_for_comment)
async def save_health_entry(message: types.Message, state: FSMContext):
    data = await state.get_data()
    comment = None if message.text.lower() == "нет" else message.text.strip()

    async for session in get_db():
        await crud.save_health(
            session=session,
            user_id=message.from_user.id,
            energy_level=data["energy_level"],
            headache=data["headache"],
            sleep_hours=data["sleep_hours"],
            comment=comment
        )

    await message.answer("Спасибо! Записал твоё самочувствие 🩺", reply_markup=ReplyKeyboardRemove())
    await state.clear()


# === Сводка ===
@router.message(Command("summary"))
async def cmd_summary(message: types.Message):
    async for session in get_db():
        moods = await get_today_moods(session, message.from_user.id)
        habits = await get_today_habits(session, message.from_user.id)
        health_entries = await get_today_health(session, message.from_user.id)
        weather_today = await crud.get_weather(session, datetime.utcnow().date(), "today")
        weather_tomorrow = await crud.get_weather(session, datetime.utcnow().date() + timedelta(days=1), "tomorrow")
        geo_today = await crud.get_geomagnetic(session, datetime.utcnow().date(), "today")
        geo_tomorrow = await crud.get_geomagnetic(session, datetime.utcnow().date() + timedelta(days=1), "tomorrow")

        # Формируем данные для анализа
        mood_data = [{"mood": m.mood, "comment": m.comment} for m in moods]
        habit_data = [{"habit": h.habit_name, "comment": h.comment} for h in habits]
        health_data = [{
            "energy_level": h.energy_level,
            "headache": h.headache,
            "sleep_hours": h.sleep_hours,
            "comment": h.comment
        } for h in health_entries]

    if not mood_data and not habit_data:
        await message.answer("У тебя пока нет данных за сегодня 🙃")
        return

    # Генерация анализа GPT
    analysis = await analyze_day(
        mood_data,
        habit_data,
        health_data,
        weather_today.to_dict() if weather_today else {},
        weather_tomorrow.to_dict() if weather_tomorrow else {},
        geo_today.to_dict() if geo_today else {},
        geo_tomorrow.to_dict() if geo_tomorrow else {},
    )
    await message.answer(f"{analysis}", parse_mode="HTML")


# === Регистрация ===
def register_handlers(dp):
    dp.include_router(router)
