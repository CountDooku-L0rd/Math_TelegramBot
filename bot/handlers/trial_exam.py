from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery
from datetime import datetime, timedelta
from asyncio import sleep


from bot.utils.db_funcs import get_exams, get_exam_tasks, get_exam_result, save_exam_result, get_exam_task, \
    is_task_solved, get_all_problems
from bot.keyboards.trial_exam import get_exam_list_keyboard, get_exam_task_keyboard, get_exam_result_keyboard, \
    get_exam_start_keyboard, get_task_nav_keyboard
from bot.utils.context import (
    set_exam_info, set_current_task, set_exam_timer, get_exam_info, get_current_task, add_user_photo, clear_context,
    set_task_feedback, user_exam_context, get_all_feedback, get_user_timer
)
from bot.utils.gpt import check_solution, give_feedback
from bot.utils.mathpix import image_to_latex
import bot

async def exam_entry(message: types.Message):
    exams = get_exams()
    await message.edit_text("Выберите экзамен:", reply_markup=get_exam_list_keyboard(exams))

async def select_exam(callback: CallbackQuery):
    await callback.answer()
    exam_id = int(callback.data.split("_")[-1])
    user_id = callback.from_user.id
    set_exam_info(user_id, exam_id=exam_id)

    exam_result = get_exam_result(exam_id, user_id)
    keyboard = get_exam_start_keyboard(exam_id)

    await callback.message.edit_text("Подтвердите начало экзамена:", reply_markup=keyboard)

async def start_exam(callback: CallbackQuery):
    user_id = callback.from_user.id
    exam_id = get_exam_info(user_id)["exam_id"]

    user_res = get_exam_result(exam_id, user_id)

    if user_res:
        await callback.answer("Экзамен уже пройден")
        return

    set_exam_info(user_id, started=True, start_dt=datetime.utcnow())

    exam_tasks = get_exam_tasks(exam_id)
    keyboard = get_exam_task_keyboard(exam_tasks)

    total_time = timedelta(hours=3,minutes=55, seconds=0)
    timer_message = callback.message
    await callback.message.answer(f"Экзамен начат! Время: {total_time}", reply_markup=keyboard)
    set_exam_timer(user_id, total_time, timer_message)

    while total_time > timedelta(0):
        if user_exam_context[user_id]["timer_message"] is None:
            break
        await sleep(1)
        total_time -= timedelta(seconds=1)
        set_exam_timer(user_id, total_time, timer_message)
        await callback.message.edit_text(f"Осталось времени: {total_time}",  parse_mode="Markdown")

    await timer_message.delete()
    await finish_exam(callback)

async def select_task(callback: CallbackQuery):
    await callback.answer()

    exam_task_id = int(callback.data.split("_")[-1])
    user_id = callback.from_user.id
    set_current_task(user_id, exam_task_id)

    exam_task = get_exam_task(exam_task_id)

    text = f"<b>Задание №{exam_task.task_order}</b>\n\n{exam_task.task_text}"
    keyboard = get_task_nav_keyboard(exam_task_id)

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="html")


async def solve_task(callback: CallbackQuery):
    user_id = callback.from_user.id
    exam_task_id = get_current_task(user_id)

    if "solved_tasks" in user_exam_context.get(user_id, {}) and exam_task_id in user_exam_context[user_id]["solved_tasks"]:
        await callback.answer("Вы уже решили этот вопрос.")
        return

    exam_task = get_exam_task(exam_task_id)

    if exam_task_id not in user_exam_context.get(user_id, {}).get("attached_photos", {}):
        await callback.answer("Пожалуйста, прикрепите фото с решением задачи.")
        return

    photo_bytes = user_exam_context[user_id]["attached_photos"][exam_task_id][0]

    user_latex = image_to_latex(photo_bytes)

    if not user_latex:
        await callback.answer("Не удалось обработать изображение.")
        return

    problem = exam_task.task_text
    feedback = check_solution(problem, user_latex)

    set_task_feedback(user_id, exam_task_id, feedback)

    del user_exam_context[user_id]["attached_photos"][exam_task_id]

    user_exam_context.setdefault(user_id, {}).setdefault("solved_tasks", []).append(exam_task_id)

    await callback.answer(f"Задание №{exam_task_id} решено!")


async def finish_exam(callback: CallbackQuery):
    user_id = callback.from_user.id
    exam_id = get_exam_info(user_id)["exam_id"]

    solved_tasks = len(user_exam_context.get(user_id, {}).get("solved_tasks", []))
    total_tasks = len(get_exam_tasks(exam_id))

    feedback = get_all_feedback(user_id)
    feedback_text = "\n\n"
    for fb in feedback:
        feedback_text.join(fb)
        feedback_text.join("\nКОНЕЦ ОЧЕРЕДНОГО ФИДБЕКА\n")

    problems = get_all_problems(exam_id)
    problems_text = "\n\n"
    for problem in problems:
        problems_text.join(problem.task_text)
        problems_text.join("\nКОНЕЦ УСЛОВИЯ ОЧЕРЕДНОГО ЗАДАНИЯ\n")

    feed = give_feedback(feedback_text, problems_text)

    save_exam_result(user_id, exam_id, solved_tasks, feed)
    timer_message, _ = get_user_timer(user_id)
    clear_context(user_id)
    if timer_message:
        await timer_message.delete()

    await callback.answer(f"Экзамен завершён! Ваш результат: {solved_tasks}/{total_tasks}")
    exams = get_exams()
    await callback.message.edit_text("Выберите экзамен:", reply_markup=get_exam_list_keyboard(exams))

async def back_to_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await bot.handlers.menu_handler.menu_comand(callback.message)

async def back_from_exam(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Выберите экзамен:", reply_markup=get_exam_list_keyboard(get_exams()))

async def back_from_task(callback: CallbackQuery):
    user_id = callback.from_user.id
    exam_task_id = get_current_task(user_id)

    if exam_task_id not in user_exam_context.get(user_id, {}).get("solved_tasks", []):
        if exam_task_id in user_exam_context.get(user_id, {}).get("attached_photos", {}):
            del user_exam_context[user_id]["attached_photos"][exam_task_id]

    exam_id = get_exam_info(user_id)["exam_id"]
    exam_tasks = get_exam_tasks(exam_id)
    keyboard = get_exam_task_keyboard(exam_tasks)

    await callback.message.edit_text("Выберите задание:", reply_markup=keyboard)

    set_current_task(user_id, None)

async def get_exam_res(callback: CallbackQuery):
    user_id = callback.from_user.id
    exam_id = int(callback.data.split("_")[-1])
    exam_res = get_exam_result(exam_id, user_id)
    if exam_res:
        await callback.message.edit_text(f"Ваш результат: {exam_res.score} решённых задач.", reply_markup=get_exam_result_keyboard(exam_res.feedback))
    else:
        await callback.answer("Экзамен ещё не решён. Результатов нет.")

async def back_from_result(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Выберите экзамен:", reply_markup=get_exam_list_keyboard(get_exams()))

async def get_fb(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    exam_id = get_exam_info(user_id)["exam_id"]
    exam_res = get_exam_result(exam_id, user_id)

    await callback.message.answer(exam_res.feedback)

def register_exam_handler(dp: Dispatcher):
    dp.register_message_handler(exam_entry, text="Пробный экзамен")
    dp.register_callback_query_handler(select_exam, lambda c: c.data.startswith("exam_choose_"))
    dp.register_callback_query_handler(start_exam, lambda c: c.data.startswith("exam_start_"))
    dp.register_callback_query_handler(select_task, lambda c: c.data.startswith("exam_task_"))
    dp.register_callback_query_handler(solve_task, lambda c: c.data.startswith("solve_task_"))
    dp.register_callback_query_handler(finish_exam, lambda c: c.data == "finish_exam")
    dp.register_callback_query_handler(back_from_exam, lambda c: c.data.startswith ("from_exam_back"))
    dp.register_callback_query_handler(get_exam_res, lambda c: c.data.startswith("exam_results"))
    dp.register_callback_query_handler(back_from_task, lambda c: c.data.startswith("exam_back_to_tasks"))
    dp.register_callback_query_handler(back_from_result, lambda c: c.data.startswith("exam_result_back"))
    dp.register_callback_query_handler(back_to_menu, lambda c: c.data == "exam_back_to_menu")
    dp.register_callback_query_handler(get_fb, lambda c: c.data.startswith("exam_result_feedback"))