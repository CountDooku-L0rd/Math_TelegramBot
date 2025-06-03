from aiogram import types, Dispatcher
from io import BytesIO
from bot.utils.context import get_user_task, user_task_context, add_user_photo, get_current_task


async def handle_practice_photo(message: types.Message):
    user_id = message.from_user.id
    task_id = get_user_task(user_id)
    if not get_user_task(user_id):
        task_id = get_current_task(user_id)

        if not task_id:
            return

        photo = message.photo[-1]
        file = await photo.download(destination=BytesIO())
        file.seek(0)
        photo_bytes = file.read()

        add_user_photo(user_id, task_id, photo_bytes, 1)
        return

    photo = message.photo[-1]
    file = await photo.download(destination=BytesIO())
    file.seek(0)
    photo_bytes = file.read()

    add_user_photo(user_id, task_id, photo_bytes, 2)

def register_photo_handlers(dp: Dispatcher):
    dp.register_message_handler(handle_practice_photo, content_types=types.ContentType.PHOTO)