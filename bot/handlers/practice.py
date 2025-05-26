from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards.practice import (get_grade_keyboard, get_subject_keyboard, get_topic_keyboard, get_task_keyboard, get_task_result_keyboard)
from bot.utils.db_funcs import (get_topics_by_class_and_subject, get_tasks_by_topic, is_task_solved, mark_task_solved)

user_practice_context = {}

async def practice_entry(message: types.Message):
    await message.answer("Выбери класс для практики:", reply_markup=get_grade_keyboard())

async def prac_select_grade(callback: CallbackQuery):
    await callback.answer()
    grade = int(callback.data.split("_")[-1])
    user_practice_context[callback.from_user.id] = {"grade": grade}
    await callback.message.edit_text("Выбери предмет:", reply_markup=get_subject_keyboard(grade))

async def prac_select_topic(callback: CallbackQuery):
    await callback.answer()
    topic_id = int(callback.data.split("_")[-1])
    user_practice_context[callback.from_user.id]["topic"] = topic_id
    tasks = get_tasks_by_topic(topic_id)
    await callback.message.edit_text("Выбери задание:", reply_markup=get_task_keyboard(tasks))

async def prac_select_task(callback: CallbackQuery):
    await callback.answer()
    task_id = int(callback.data.split("_")[-1])
    user_id = callback.from_user.id
    task_done = is_task_solved(user_id, task_id)
    await callback.message.edit_text(f"<b>Задача:</b>\n\nID: {task_id}", reply_markup=get_task_result_keyboard(task_id, task_done), parse_mode="html")

async def prac_submit(callback: CallbackQuery):
    await callback.answer()
    task_id = int(callback.data.split("_")[-1])
    user_id = callback.from_user.id
    mark_task_solved(user_id, task_id)
    await callback.message.edit_text(f"Задача проверена!\n\nРешение верно.\n\nЗадача зачтена.", reply_markup=get_task_result_keyboard(task_id, True))

async def prac_ignore(callback: CallbackQuery):
    await callback.answer("Эта задача уже решена")
