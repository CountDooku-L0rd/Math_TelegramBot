from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery
from sqlalchemy.sql.functions import user

from bot.utils.db_funcs import get_topics_by_class_and_subject, is_topic_read, mark_topic_as_read
from bot.keyboards.theory import get_grade_keyboard, get_subject_keyboard, get_topic_keyboard, get_topics_by_class_and_subject, get_theory_nav_keyboard

user_context = {}

async def theory_entry(message: types.Message):
    await message.answer("Выбери класс:", reply_markup=get_grade_keyboard())

async def select_grade(callback: CallbackQuery):
    grade = int(callback.data.split("_")[1])
    user_context[callback.from_user.id] = {"grade": grade}
    await callback.message.edit_text("Выбери предмет:", reply_markup=get_subject_keyboard(grade))

async def select_subject(callback: CallbackQuery):
    subject = callback.data.split("_")[0]
    user_context[callback.from_user.id]["subject"] = subject
    grade = user_context[callback.from_user.id]["grade"]
    topics = get_topics_by_class_and_subject(grade, subject)
    if not topics:
        await callback.message.answer("Для этого класса и предмета нет тем для изучения.")
        return

    await callback.message.edit_text("Выбери тему", reply_markup=get_topic_keyboard(topics))

async def select_topic(callback: CallbackQuery):
    topic_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id
    from bot.utils.db_funcs import SessionLocal
    from bot.models.models import Topic
    sesion = SessionLocal()
    topic = sesion.query(Topic).filter(Topic.id == topic_id).first()
    sesion.close()
    if not topic:
        await callback.message.answer("Выбранной темы не сущестует!")
        return
    read = is_topic_read(user_id, topic_id)
    text = f"<b>{topic.topic_title}<b>\n\n{topic.topic_conspect}"
    await callback.message.answer(text, reply_markup=get_theory_nav_keyboard(), parse_mode="html")

async def toggle_read(callback: CallbackQuery):
    data = callback.data.split("_")
    topic_id = int(data[1])
    action = data[2]
    user_id = callback.from_user.id
    from bot.utils.db_funcs import SessionLocal, UserTopicProgress
    sesion = SessionLocal()
    if action == "mark":
        if not is_topic_read(user_id, topic_id):
            mark_topic_as_read(user_id, topic_id)
        await callback.answer("Тема отмечена как прочитанная")
    elif action == "unmark":
        row = sesion.query(UserTopicProgress).filter(user_id == user_id, topic_id = topic_id).first()
        if row:
            sesion.delete(row)
            sesion.commit()
        await callback.answer("Отметка снята")
    sesion.close()
    await  callback.message.delete()

def register_theory_handler(dp: Dispatcher):
    dp.register_message_handler(theory_entry, text="Теория")
    dp.register_callback_query_handler(select_grade, lambda c: c.data.startswith("grade_"))
    dp.register_callback_query_handler(select_subject, lambda c: c.data.startswith(("alg_", "geom_", "math_")))
    dp.register_callback_query_handler(select_topic, lambda c: c.data.startswith("topic_"))
    dp.register_callback_query_handler(toggle_read, lambda c: c.data.startswith("read_"))