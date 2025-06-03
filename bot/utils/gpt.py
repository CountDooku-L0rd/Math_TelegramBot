import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def check_solution(problem: str, user_latex:str) -> str:
    prompt = f"""
Пользователь решил следующую задачу по математике:

Задача:
{problem}

Решение (в виде формул LaTeX):
{user_latex}

Оцени это решение: правильно оно или нет? Объясни почему. Дай чёткий вердикт (Правильно / Неправильно).

Дай подробный, но краткий анализ.

Также, в конце, опиши кратко что конкретно было сделано в решении.
"""
    response = client.completions.create(
        model = "gpt-3.5-turbo-instruct",
        prompt = prompt,
        #messages=[{"role": "user", "content": prompt}],
        max_tokens = 500,
        temperature = 0.3,
    )
    return response.choices[0].text.strip()

def give_feedback(feedbacks, problems) ->str:
    prompt = f"""
    Пользователь решал экзамен по математике и были даны следующие анализы решения его задач:

    Все формулировки заданий:
    {problems}

    Все фидбеки по решениям заданий (Смотри по контексту какой фидбек за что отвечает):
    {feedbacks}

    Оцени эти решения и весь экзамен по 100 бальной шкале. Исходи из количества и правильности решённых задач. Дай фидбек (Какие темы было бы неплохо подучить, сильные и слабые стороны пользователя)
    Если задача не решена, или решена неверно предложи своё решение.
    Постарайся быть коротким и представь что ты учитель который общается с обычным учеником, а сам проверяешь решение из бумажной тетради.

    Дай подробный, но краткий анализ.
    """
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        # messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.3,
    )
    return response.choices[0].text.strip()