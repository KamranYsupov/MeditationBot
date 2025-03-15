import os
from typing import Callable

from aiogram import Bot


def get_bot_method_by_file_extension(
        bot: Bot,
        file_name: str,
) -> Callable:
    file_ext = os.path.splitext(file_name)[1].lower()

    if file_ext == '.mp4':
        return bot.send_video

    elif file_ext == '.mp3':
        return bot.send_audio

    elif file_ext in ('.jpg', '.jpeg', '.png'):
        return bot.send_photo
