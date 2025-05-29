import os

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import Message
from aiogram.utils import executor
from dotenv import load_dotenv
from bot.handlers.menu_handler import register_menu_handlers
from bot.handlers.theory import register_theory_handler
from bot.utils.db_funcs import register_user
from bot.handlers.practice import register_practice_handlers
from bot.handlers.photo import handle_photo, register_photo_handlers

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token = BOT_TOKEN)
dp = Dispatcher(bot)

register_menu_handlers(dp)
register_theory_handler(dp)
register_practice_handlers(dp)
register_photo_handlers(dp)

@dp.message_handler(commands=["start"])
async def start_command(message: Message):
    register_user(message.from_user.id, message.from_user.username)
    await message.answer("Привет! Это чат-бот для подготовки к ЕГЭ по математике")

if __name__ == '__main__':
    print("Бот успешно запущен, ожидаю сообщения")
    executor.start_polling(dp, skip_updates=True)