from datetime import datetime
from bot.utils.db import SessionLocal
from bot.models.models import User, Topic, UserTopicProgres, Task, Result, Exam, ExamTask, ExamResult
from datetime import datetime
from typing import List

def register_user(telegram_id:int, username: str = None):
    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        user = User(telegram_id=telegram_id, username=username, registred_at=datetime.utcnow())
        session.add(user)
        session.commit()
    session.close()


def get_topics_by_class_and_subject(grade: int, subject: str):
    session = SessionLocal()
    topics = session.query(Topic).filter_by(grade=grade, subject=subject).all()
    session.close()
    return topics

def mark_topic_as_read(user_id: int, topic_id: int):
    session = SessionLocal()
    exists = session.query(UserTopicProgres).filter_by(user_id=user_id, topic_id=topic_id).first()
    if not exists:
        mark = UserTopicProgres(user_id=user_id, topic_id=topic_id, marked_at=datetime.utcnow())
        session.add(mark)
        session.commit()
    session.close()

def is_topic_read(user_id: int, topic_id: int) -> bool:
    session = SessionLocal()
    exists = session.query(UserTopicProgres).filter_by(user_id=user_id, topic_id=topic_id).first()
    session.close()
    return exists is not None

def get_tasks_by_topic(topic_id: int):
    session = SessionLocal()
    tasks = session.query(Task).filter_by(topic_id=topic_id).all()
    session.close()
    return tasks

def save_task_result(user_id: int, task_id: int, is_correct: int):
    session = SessionLocal()
    result = Result(user_id=user_id, task_id=task_id, is_correct=is_correct, answered_at=datetime.utcnow())
    session.add(result)
    session.commit()
    session.close()

def get_exam_by_id(exam_id: int):
    session = SessionLocal()
    exam = session.query(Exam).filter_by(exam_id=exam_id).first()
    session.close()
    return exam

def get_task_by_id(task_id:int):
    session = SessionLocal()
    task = session.query(Task).filter_by(task_id=task_id).first()
    session.close()
    return task


def get_exam_tasks(exam_id: int):
    session = SessionLocal()
    tasks = session.query(ExamTask).filter_by(exam_id=exam_id).order_by(ExamTask.task_order).all()
    session.close()
    return tasks

def get_exam_task(exam_task_id: int):
    session = SessionLocal()
    tasks = session.query(ExamTask).filter_by(exam_task_id=exam_task_id).order_by(ExamTask.exam_task_id).first()
    session.close()
    return tasks

def get_exams():
    session = SessionLocal()
    exams = session.query(Exam).order_by(Exam.exam_id).all()
    session.close()
    return exams

def get_all_problems(exam_id: int):
    session = SessionLocal()
    problems = session.query(ExamTask).filter_by(exam_id=exam_id).all()
    session.close()
    return problems

def get_exam_result(exam_id: int, user_id: int):
    session = SessionLocal()
    exam_results = session.query(ExamResult).filter_by(exam_id=exam_id, user_id=user_id).first()
    session.close()
    return exam_results


def save_exam_result(user_id: int, exam_id: int, score: int, feedback:str):
    session = SessionLocal()
    result = ExamResult(user_id = user_id, exam_id = exam_id, score = score, completed_at=datetime.utcnow(), feedback=feedback)
    session.add(result)
    session.commit()
    session.close()

def is_task_solved(task_id: int):
    session = SessionLocal()

def is_task_solved(user_id:int, task_id:int) -> bool:
    session = SessionLocal()
    result = session.query(Result).filter_by(user_id = user_id, task_id=task_id, is_correct=True).first()
    session.close()
    return result is not None

def mark_task_solved(user_id:int, task_id:int) -> None:
    session = SessionLocal()
    existing = session.query(Result).filter_by(user_id=user_id, task_id=task_id, is_correct=True).first()
    if not existing:
        result = Result(user_id = user_id, task_id = task_id, is_correct = True, answered_at = datetime.utcnow())
        session.add(result)
        session.commit()
    session.close()

def get_tasks_by_topic(topic_id: int) -> List[Task]:
    session = SessionLocal()
    tasks = session.query(Task).filter_by(topic_id=topic_id).all()
    session.close()
    return tasks