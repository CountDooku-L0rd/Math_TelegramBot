from collections import defaultdict

user_task_context = {}

def set_user_task(user_id:int, task_id:int):
    user_task_context.setdefault(user_id, {})
    user_task_context[user_id]["current_task_id"] = task_id

def get_user_task(user_id:int):
    return user_task_context.get(user_id, {}).get("current_task_id")

def add_user_photo(user_id:int, task_id:int, photo_bytes:bytes):
    user_task_context.setdefault(user_id, {})
    user_task_context[user_id].setdefault("attached_photos", {})
    user_task_context[user_id]["attached_photos"].setdefault(task_id, []).append(photo_bytes)

def get_user_photo(user_id:int, task_id:int):
    return user_task_context.get(user_id, {}).get("attached_photos", {}).get(task_id, [])

def clear_user_context(user_id:int, task_id:int):
    if user_id in user_task_context and "attached_photos" in user_task_context[user_id]:
        user_task_context[user_id]["attached_photos"].pop(task_id, None)