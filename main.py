import os

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token = BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: Message):
    await message.answer("Привет! Это чат-бот для подготовки к ЕГЭ по математике")

if __name__ == '__main__':
    print("Бот успешно запущен, ожидаю сообщения")
    executor.start_polling(dp, skip_updates=True)