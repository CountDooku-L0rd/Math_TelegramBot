from sqlalchemy import Column, Integer, String, Text, DateTime, SMALLINT, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    telegram_id = Column(BigInteger, primary_key=True)
    username = Column(String, nullable=False)
    registred_at = Column(DateTime, nullable=False)

class Topic(Base):
    __tablename__ = "topics"
    topic_id = Column(Integer, primary_key=True, autoincrement=True)
    topic_title = Column(String, nullable=False)
    topic_conspect = Column(Text, nullable=False)
    grade = Column(Integer, nullable=False)
    subject = Column(String, nullable=False)
    video_url = Column(String, nullable=True)

class Task(Base):
    __tablename__ = "tasks"
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    topic_id = Column(Integer, ForeignKey("topics.topic_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    task_text = Column(Text, nullable=False)
    difficulty = Column(Integer, nullable=False)

class Result(Base):
    __tablename__ = "results"
    result_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.task_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    is_correct = Column(SMALLINT, nullable=False)
    answered_at = Column(DateTime, nullable=False)

class UserTopicProgres(Base):
    __tablename__ = "user_topic_progres"
    topic_progres_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.topic_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    marked_at = Column(DateTime, nullable=False)

class Exam(Base):
    __tablename__ = "exams"
    exam_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

class ExamTask(Base):
    __tablename__ = "exam_task"
    exam_task_id = Column(Integer, primary_key=True, autoincrement=True)
    exam_id = Column(Integer, ForeignKey("exams.exam_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    task_order = Column(Integer, nullable=False)
    task_text = Column(Text, nullable=False)
    task_type = Column(String, nullable=False)

class ExamResult(Base):
    __tablename__ = "exam_results"
    exam_res_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    exam_id = Column(Integer, ForeignKey("exams.exam_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, nullable=False)
    completed_at = Column(DateTime, nullable=False)
    feedback = Column(Text, nullable=False)

class Admin(Base):
    __tablename__ = "admins"
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    password = Column(String, nullable=False)