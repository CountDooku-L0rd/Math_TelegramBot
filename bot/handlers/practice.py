from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards.practice import (get_prac_grade_keyboard, get_prac_subject_keyboard, get_prac_topic_keyboard, get_task_keyboard, get_task_result_keyboard)
from bot.utils.db_funcs import (get_topics_by_class_and_subject, get_tasks_by_topic, is_task_solved, mark_task_solved, get_task_by_id)
from aiogram.dispatcher import FSMContext
from bot.utils.mathpix import image_to_latex
from bot.utils.gpt import check_solution
from bot.utils.context import user_task_context, get_user_photo, get_user_task, set_user_task, clear_user_context
from io import BytesIO
import bot.handlers.menu_handler
from bot.utils.context import user_task_context

user_practice_context = {}

async def practice_entry(message: types.Message):
    await message.edit_text("Выбери класс для практики:", reply_markup=get_prac_grade_keyboard())

async def prac_select_grade(callback: CallbackQuery):
    await callback.answer()
    grade = int(callback.data.split("_")[-1])
    user_practice_context[callback.from_user.id] = {"grade": grade}
    await callback.message.edit_text("Выбери предмет для практики:", reply_markup=get_prac_subject_keyboard(grade))

async def prac_select_subject(callback: CallbackQuery):
    await callback.answer()
    subject = callback.data.split("_")[0]
    user_practice_context[callback.from_user.id]["subject"] = subject
    grade = user_practice_context[callback.from_user.id]["grade"]
    topics = get_topics_by_class_and_subject(grade, subject)

    if not topics:
        await callback.message.edit_text("Для этого класса и предмета нет тем для практики.")
        return

    await callback.message.edit_text("Выбери тему для практики: ", reply_markup=get_prac_topic_keyboard(topics))

async def prac_select_topic(callback: CallbackQuery):
    await callback.answer()
    topic_id = int(callback.data.split("_")[-1])
    user_practice_context[callback.from_user.id]["topic"] = topic_id
    tasks = get_tasks_by_topic(topic_id)
    await callback.message.edit_text("Выбери задание:", reply_markup=get_task_keyboard(tasks))

async def prac_select_task(callback: CallbackQuery):
    await callback.answer()
    task_id = int(callback.data.split("_")[-1])
    task = get_task_by_id(task_id)
    user_id = callback.from_user.id
    task_done = is_task_solved(user_id, task_id)
    set_user_task(user_id, task_id)
    await callback.message.edit_text(f"<b>Задача: {task_id}</b>\n\n{task.task_text}", reply_markup=get_task_result_keyboard(task_id, task_done), parse_mode="html")

async def prac_submit(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    task_id = get_user_task(user_id)
    if task_id is None:
        await callback.answer("Сначала выберите задание")
        return
    photos = get_user_photo(user_id, task_id)
    if not photos:
        await callback.answer("Нет прикреплённых фото.")
        return

    await callback.answer("Обрабатываю решение...")

    latex_parts = []
    for img in photos:
        try:
            latex = image_to_latex(img)
            if latex:
                latex_parts.append(latex)
        except Exception as e:
            await callback.answer("Ошибка при обработке фото.")
            return

        task = get_task_by_id(task_id)

        if not task:
            await callback.answer("Задание не выбрано.")
            return

    result = check_solution(task.task_text, "$$\n" + "\n".join(latex_parts) + "\n$$")
    user_task_context[user_id]["images"] = []
    await callback.message.answer(f"Результат проверки:\n\n{result}")

    verdict_text = result.lower()
    is_correct = (
        "прав" in verdict_text and
        "неправ" not in verdict_text.split()[0]
    )
    if is_correct:
        mark_task_solved(user_id, task_id)
        await callback.message.edit_text(f"Задача проверена!\n\nРешение верно.\n\nЗадача зачтена.", reply_markup=get_task_result_keyboard(task_id, True))
    else:
        await callback.message.answer(f"Задача решена неверно!!!")
        clear_user_context(user_id, task_id)

async def prac_ignore(callback: CallbackQuery):
    await callback.answer("Эта задача уже решена")

async def prac_back_sybject(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Выбери класс для практики:", reply_markup=get_prac_grade_keyboard())

async def prac_back_topics(callback: CallbackQuery):
    await callback.answer()
    grade = user_practice_context.get(callback.from_user.id, {}).get("grade")
    await callback.message.edit_text("Выбери предмет для практики:", reply_markup=get_prac_subject_keyboard(grade))

async def prac_back_tasks(callback: CallbackQuery):
    await callback.answer()
    context = user_practice_context.get(callback.from_user.id)
    topics = get_topics_by_class_and_subject(context["grade"], context["subject"])
    await callback.message.edit_text("Выбери тему для практики:", reply_markup=get_prac_topic_keyboard(topics))

async def prac_back_task(callback: CallbackQuery):
    await callback.answer()
    context = user_practice_context.get(callback.from_user.id)
    tasks = get_tasks_by_topic(context["topic"])
    await callback.message.edit_text("Выбери задание для практики:", reply_markup=get_task_keyboard(tasks))

async def back_to_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await bot.handlers.menu_handler.menu_comand(callback.message)

def register_practice_handlers(dp: Dispatcher):
    dp.register_message_handler(practice_entry, text="Практика")
    dp.register_callback_query_handler(prac_select_grade, lambda c: c.data.startswith("prac_grade_"))
    dp.register_callback_query_handler(prac_select_subject, lambda c: c.data.startswith(("alg_prac_", "geom_prac_", "math_prac_")))
    dp.register_callback_query_handler(prac_select_topic, lambda c: c.data.startswith("prac_topic_"))
    dp.register_callback_query_handler(prac_select_task, lambda c: c.data.startswith("prac_task_"))
    dp.register_callback_query_handler(prac_submit, lambda c: c.data.startswith("prac_submit_"))
    dp.register_callback_query_handler(prac_back_sybject, lambda c: c.data=="prac_back_to_grades")
    dp.register_callback_query_handler(prac_back_topics, lambda c: c.data=="prac_back_to_subjects")
    dp.register_callback_query_handler(prac_back_tasks, lambda c: c.data=="prac_back_to_topics")
    dp.register_callback_query_handler(prac_back_task, lambda c: c.data=="prac_back_to_tasks")
    dp.register_callback_query_handler(prac_ignore, lambda c: c.data=="ignore")
    dp.register_callback_query_handler(back_to_menu, lambda c: c.data=="prac_back_to_menu")