from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from asgiref.sync import sync_to_async

from web.db.model_mixins import (
    AsyncBaseModel,
    TimestampMixin
)


class Notification(AsyncBaseModel, TimestampMixin):
    """Модель рассылки"""

    file = models.FileField(
        _('Фото/Аудиофайл/Видео'),
        upload_to='notifications/',
        null=True,
        blank=True,
        default=None
    )
    text = models.TextField(_('Текст'), max_length=1000)

    updated_at = None
