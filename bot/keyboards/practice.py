from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_grade_keyboard():
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(InlineKeyboardButton("Назад", callback_data="back_to_menu"))
    for i in range(1,12):
        markup.insert(InlineKeyboardButton(str(i), callback_data=f"prac_grade_{i}"))
    return markup

def get_subject_keyboard(grade):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Назад", callback_data=f"back_to_grades"))
    if grade>=7:
        markup.add(InlineKeyboardButton(f"Алгебра {grade} класс", callback_data=f"alg_prac_{grade}"))
        markup.add(InlineKeyboardButton(f"Геометрия {grade} класс", callback_data=f"geom_prac_{grade}"))
    else:
        markup.add(InlineKeyboardButton(f"Математика {grade} класс", callback_data=f"math_prac_{grade}"))
    return markup

def get_topic_keyboard(topics):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Назад", callback_data=f"back_to_subjects"))
    for topic in topics:
        markup.add(InlineKeyboardButton(topic.topic_title, callback_data=f"topic_{topic.topic_id}"))
    return markup

def get_task_keyboard(tasks):
    markup = InlineKeyboardMarkup()
    i = 1
    markup.add(InlineKeyboardButton("Назад", callback_data=f"back_to_topics"))
    for task in tasks:
        markup.add(InlineKeyboardButton(f"Задание №{i} \nСложность: {task.difficulty}", callback_data=f"task_{task.task_id}"))
        i = i + 1
    return markup

def get_task_result_keyboard(task_id, is_done:bool):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Назад", callback_data=f"back_to_tasks"))
    if not is_done:
        markup.add(InlineKeyboardButton("Отправить на проверку", callback_data=f"prac_submit_{task_id}"))
    else:
        markup.add(InlineKeyboardButton("Задача уже решена", callback_data=f"ignore"))
    return markup
