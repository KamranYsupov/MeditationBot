from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from asgiref.sync import sync_to_async

from web.db.model_mixins import (
    AsyncBaseModel,
    TimestampMixin
)
from web.validators.file import FileValidator


class Notification(AsyncBaseModel, TimestampMixin):
    """Модель рассылки"""

    file = models.FileField(
        _('Фото/Аудиофайл/Видео'),
        upload_to='notifications/',
        validators=[FileValidator()],
        null=True,
        blank=True,
        default=None
    )
    text = models.TextField(_('Текст'), max_length=1000)
    receivers = models.ManyToManyField(
        'telegram_users.TelegramUser',
        verbose_name=_('Получатели')
    )

    updated_at = None

    class Meta:
        verbose_name = _('Рассылка')
        verbose_name_plural = _('Рассылки')
        ordering = ['-created_at']

    def __str__(self):
        return self.text[:100]
