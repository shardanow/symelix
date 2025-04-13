from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

mood_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="😊"), KeyboardButton(text="😐"), KeyboardButton(text="😢")],
        [KeyboardButton(text="😡"), KeyboardButton(text="🤯")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
