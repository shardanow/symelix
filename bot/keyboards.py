from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

mood_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="😊 Радость"), KeyboardButton(text="😐 Нейтрально"), KeyboardButton(text="😢 Печально")],
        [KeyboardButton(text="😡 Злость"), KeyboardButton(text="🤯 Стресс")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

habit_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💧 Вода"), KeyboardButton(text="💊 Витамины")],
        [KeyboardButton(text="🚶‍♂️ Прогулка"), KeyboardButton(text="🧘 Отдых от экрана")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

energy_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=str(i)) for i in range(1, 6)],
        [KeyboardButton(text=str(i)) for i in range(6, 11)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

headache_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Да"), KeyboardButton(text="Нет")]],
    resize_keyboard=True,
    one_time_keyboard=True
)

yes_no_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
