import asyncio
import os

from aiogram.types import FSInputFile
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from bot.loader import bot
from bot.utils.message import get_bot_method_by_file_extension
from .models import Notification
from ...services.telegram import telegram_service


@receiver(post_save, sender=Notification)
def send_notification_after_creation(sender, instance: Notification, created, **kwargs):
    if not created:
        return

    file_ext = os.path.splitext(instance.file.name)[1].lower()
    if file_ext == '.mp4':
        method, file_type = ('sendVideo', 'video')
    elif file_ext == '.mp3':
        method, file_type = ('sendAudio', 'audio')
    elif file_ext in ('.jpg', '.jpeg', '.png'):
        method, file_type = ('sendPhoto', 'photo')
    else:
        return

    def send_notification():
        for telegram_user in instance.receivers.all():
            telegram_service.send_file(
                chat_id=telegram_user.telegram_id,
                file_path=instance.file.path,
                file_type=file_type,
                method=method,
                caption=instance.text
            )

    transaction.on_commit(send_notification)