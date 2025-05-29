from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils.db_funcs import get_topics_by_class_and_subject

def get_grade_keyboard():
    markup = InlineKeyboardMarkup(row_width = 3)
    markup.add(InlineKeyboardButton("Назад", callback_data="theory_back_to_menu"))
    buttons = [InlineKeyboardButton(str(i), callback_data=f"theory_grade_{i}") for i in range (1, 12)]
    markup.add(*buttons)
    return markup

def get_subject_keyboard(grade):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Назад", callback_data="theory_back_to_grade"))
    if (grade >= 7):
        markup.add(
            InlineKeyboardButton(f"Алгебра {grade} класс", callback_data=f"alg_theory_{grade}"),
            InlineKeyboardButton(f"Геометрия {grade} класс", callback_data=f"geom_theory_{grade}")
        )
    else:
        markup.add(
            InlineKeyboardButton(f"Математика {grade} класс", callback_data=f"math_theory_{grade}")
        )
    return markup

def get_topic_keyboard(topics):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Назад", callback_data="theory_back_to_subject"))
    for topic in topics:
        markup.add(InlineKeyboardButton(topic.topic_title, callback_data=f"theory_topic_{topic.topic_id}"))
    return markup

def get_theory_nav_keyboard(topic_id: int, is_read: bool):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Назад", callback_data="theory_back_to_topics"))
    if is_read:
        markup.add(InlineKeyboardButton("Убрать отметку", callback_data=f"read_{topic_id}_unmark"))
    else:
        markup.add(InlineKeyboardButton("Отметить прочитанным", callback_data=f"read_{topic_id}_mark"))
    return markup
