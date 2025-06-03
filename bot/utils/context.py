from collections import defaultdict
from datetime import datetime, timedelta

user_task_context = {}
user_exam_context = {}


def set_user_task(user_id:int, task_id:int):
    user_task_context.setdefault(user_id, {})
    user_task_context[user_id]["current_task_id"] = task_id

def get_user_task(user_id:int):
    return user_task_context.get(user_id, {}).get("current_task_id")


def get_user_photo(user_id:int, task_id:int):
    return user_task_context.get(user_id, {}).get("attached_photos", {}).get(task_id, [])

def clear_user_context(user_id:int, task_id:int):
    if user_id in user_task_context and "attached_photos" in user_task_context[user_id]:
        user_task_context[user_id]["attached_photos"].pop(task_id, None)

def set_exam_info(user_id, exam_id=None, started=None, finished=None, start_dt=None):
    user_exam_context.setdefault(user_id, {})
    if exam_id is not None:
        user_exam_context[user_id]["exam_id"] = exam_id
    if started is not None:
        user_exam_context[user_id]["started"] = started
    if finished is not None:
        user_exam_context[user_id]["finished"] = finished
    if start_dt is not None:
        user_exam_context[user_id]["start_dt"] = start_dt

def get_exam_info(user_id):
    return user_exam_context.get(user_id, {})

def set_current_task(user_id, exam_task_id):
    user_exam_context.setdefault(user_id, {})
    user_exam_context[user_id]["current_task_id"] = exam_task_id

def get_current_task(user_id):
    return user_exam_context.get(user_id, {}).get("current_task_id")

def set_exam_timer(user_id, time_left):
    user_exam_context.setdefault(user_id, {})
    user_exam_context[user_id]["time_left"] = time_left

def get_exam_timer(user_id):
    return user_exam_context.get(user_id, {}).get("time_left", timedelta(0))

def add_user_photo(user_id, task_id, photo_bytes, type):
    if type == 1:
        user_exam_context.setdefault(user_id, {})
        user_exam_context[user_id].setdefault("attached_photos", {})
        user_exam_context[user_id]["attached_photos"].setdefault(task_id, []).append(photo_bytes)
    elif type == 2:
        user_task_context.setdefault(user_id, {})
        user_task_context[user_id].setdefault("attached_photos", {})
        user_task_context[user_id]["attached_photos"].setdefault(task_id, []).append(photo_bytes)

def clear_context(user_id):
    if user_id in user_exam_context:
        del user_exam_context[user_id]

def set_task_feedback(user_id, exam_task_id, feedback):
    user_exam_context.setdefault(user_id, {})
    user_exam_context[user_id].setdefault("task_feedback", {})
    user_exam_context[user_id]["task_feedback"][exam_task_id] = feedback

def get_all_feedback(user_id):
    feedbacks = []

    task_feedbacks = user_exam_context.get(user_id, {}).get("task_feedback", {})

    for exam_task_id, feedback in task_feedbacks.items():
        feedbacks.append(f"Задание {exam_task_id}:\n{feedback}")

    return feedbacks