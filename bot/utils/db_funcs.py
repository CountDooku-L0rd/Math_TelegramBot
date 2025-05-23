from datetime import datetime
from bot.utils.db import SessionLocal
from bot.models.models import User, Topic, UserTopicProgres, Task, Result, Exam, ExamTask, ExamResult

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

def get_exam_tasks(exam_id: int):
    session = SessionLocal()
    tasks = session.query(ExamTask).filter_by(exam_id=exam_id).order_by(ExamTask.task_order).all()
    session.close()
    return tasks

def save_exam_result(user_id: int, exam_id: int, score: int):
    session = SessionLocal()
    result = ExamResult(user_id = user_id, exam_id = exam_id, score = score, completed_at=datetime.utcnow())
    session.add(result)
    session.commit()
    session.close()