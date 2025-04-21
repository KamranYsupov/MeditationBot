import asyncio
import os

from aiogram.types import FSInputFile
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from .models import Notification
from ...services.telegram import telegram_service


@receiver(post_save, sender=Notification)
def send_notification_after_creation(sender, instance: Notification, created, **kwargs):
    if not created:
        return

    def send_notification():
        if not instance.file:
            telegram_method = telegram_service.send_message
            telegram_method_kwargs = dict(text=instance.text)
        else:
            file_ext = os.path.splitext(instance.file.name)[1].lower()
            if file_ext == '.mp4':
                method, file_type = ('sendVideo', 'video')
            elif file_ext == '.mp3':
                method, file_type = ('sendAudio', 'audio')
            elif file_ext in ('.jpg', '.jpeg', '.png'):
                method, file_type = ('sendPhoto', 'photo')
            else:
                return

            telegram_method = telegram_service.send_file
            telegram_method_kwargs = dict(
                file_path=instance.file.path,
                file_type=file_type,
                method=method,
                caption=instance.text,
            )

        for telegram_user in instance.receivers.all():
            telegram_method_kwargs['chat_id'] = telegram_user.telegram_id
            print(telegram_method_kwargs)
            telegram_method(**telegram_method_kwargs)

    transaction.on_commit(send_notification)