from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.handlers.theory import theory_entry

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
    await callback.answer()
    if data == "theory":
        await theory_entry(callback.message)
    elif data == "practice":
        await callback.message.answer("Раздел практики ещё в разработке")
    elif data == "trial_exam":
        await callback.message.answer("Раздел экзаменов ещё в разработке")
    elif data == "ai_consult":
        await callback.message.answer("Раздел пробного экзамена ещё в разработке")
    elif data == "help":
        await callback.message.answer("Раздел помощи ещё в разработке")
    else:
        await callback.message.answer("Неизвестная команда")

def register_menu_handlers(dp: Dispatcher):
    dp.register_message_handler(menu_comand, commands=["menu"])
    dp.register_callback_query_handler(menu_callback, lambda c: c.data in ["theory", "practice", "trial_exam", "ai_consult", "help"])