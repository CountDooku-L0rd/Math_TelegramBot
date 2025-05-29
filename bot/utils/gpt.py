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
"""
    response = client.completions.create(
        model = "gpt-3.5-turbo-instruct",
        prompt = prompt,
        #messages=[{"role": "user", "content": prompt}],
        max_tokens = 500,
        temperature = 0.3,
    )
    return response.choices[0].text.strip()