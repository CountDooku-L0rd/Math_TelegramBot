from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_exam_list_keyboard(exams):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("Назад", callback_data="exam_back_to_menu"))
    for exam in exams:
        markup.add(InlineKeyboardButton(exam.title, callback_data=f"exam_choose_{exam.exam_id}"))
    return markup

def get_exam_start_keyboard(exam_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Начать экзамен", callback_data=f"exam_start_{exam_id}"))
    markup.add(InlineKeyboardButton("Результаты", callback_data=f"exam_results_{exam_id}"))
    markup.add(InlineKeyboardButton("Назад", callback_data=f"from_exam_back_{exam_id}"))
    return markup

def get_exam_task_keyboard(exam_tasks):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("Завершить экзамен", callback_data="finish_exam"))
    for task in exam_tasks:
        markup.add(InlineKeyboardButton(f"Задание №{task.task_order}", callback_data=f"exam_task_{task.exam_task_id}"))
    return markup

def get_task_nav_keyboard(exam_task_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Отправить решение", callback_data=f"solve_task_{exam_task_id}"))
    markup.add(InlineKeyboardButton("Назад", callback_data="exam_back_to_tasks"))
    return markup

def get_exam_result_keyboard(feedback):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(f"Фидбек", callback_data="exam_result_feedback"))
    markup.add(InlineKeyboardButton(f"Назад", callback_data="exam_result_back"))
    return markup