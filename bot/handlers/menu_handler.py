from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.handlers.theory import theory_entry
from bot.handlers.practice import practice_entry
from bot.handlers.trial_exam import exam_entry


async def menu_comand (message: types.Message):
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton("Теория", callback_data="theory"),
        InlineKeyboardButton("Практика", callback_data="practice"),
        InlineKeyboardButton("Пробный ЕГЭ", callback_data="trial_exam"),
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
        await practice_entry(callback.message)
    elif data == "trial_exam":
        await exam_entry(callback.message)
    elif data == "help":
        await callback.message.answer("Для того чтобы изучать теорию - жми на ТЕОРИЯ\nЕсли хочешь подтягуть знания на практике - жми на ПРАКТИКА\nЕсли же думаешь что готов испытать себя на пробных экзаменах - жми Пробный ЕГЭ")
    else:
        await callback.message.answer("Неизвестная команда")

def register_menu_handlers(dp: Dispatcher):
    dp.register_message_handler(menu_comand, commands=["menu"])
    dp.register_callback_query_handler(menu_callback, lambda c: c.data in ["theory", "practice", "trial_exam", "help"])