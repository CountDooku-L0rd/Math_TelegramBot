from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_grade_keyboard():
    markup = InlineKeyboardMarkup(now_width = 3)
    buttons = [InlineKeyboardButton(str(i), callback_data=f"grade_{i}") for i in range (1, 12)]
    markup.add(*buttons)
    return markup

def get_subject_keyboard(grade):
    markup = InlineKeyboardMarkup()
    if (grade >= 7):
        markup.add(
            InlineKeyboardButton(f"Алгебра {grade} класс", callback_data=f"alg_{grade}"),
            InlineKeyboardButton(f"Геометрия {grade} класс", callback_data=f"geom_{grade}")
        )
    else:
        markup.add(
            InlineKeyboardButton(f"Математика {grade} класс", callback_data=f"math_{grade}")
        )
    return markup

def get_topic_keyboard(grade, subject):
    markup = InlineKeyboardMarkup()
    topics = ["деление", "дроби", "формулы"]
    for topic in topics:
        markup.add(InlineKeyboardButton(topic.title(), callback_data=f"topic_{grade}_{subject}_{topic}"))
    return markup

def get_theory_nav_keyboard(topic_key):
    markup = InlineKeyboardMarkup()
