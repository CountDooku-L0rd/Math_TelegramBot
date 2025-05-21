from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def menu_comand (message: types.Message):
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton("Теория", callback_data="theory"),
        InlineKeyboardButton("Практика", callback_data="practice"),
        InlineKeyboardButton("Пробный ЕГЭ", callback_data="trial_exam"),
        InlineKeyboardButton("AI-консультант", callback_data="ai_consult"),
        InlineKeyboardButton("Помощь", callback_data="help"),
    ]
    markup.add(*buttons)
    await message.answer("Выберите раздел:", reply_markup=markup)

async def menu_callback (callback: types.CallbackQuery):
    data = callback.data
    response_map = {
        "theory": "Раздел теории ещё в разработке",
        "practice": "Раздел практика ещё в разработке",
        "trial_exam": "Раздел пробный ЕГЭ ещё в разработке",
        "ai_consult": "Раздел консультации с ИИ ещё в разработке",
        "help": "Это чат-бот для подготовке к профильному ЕГЭ по математике, выбирай раздел и вперёд!"
    }
    await callback.answer()
    await callback.message.answer(response_map.get(data, "Неизвестная команда"))

def register_menu_handlers(dp: Dispatcher):
    dp.register_message_handler(menu_comand, commands=["menu"])
    dp.register_callback_query_handler(menu_callback)