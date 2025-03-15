from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from asgiref.sync import sync_to_async

from web.db.model_mixins import (
    AsyncBaseModel,
)


class Meditation(AsyncBaseModel):
    """Модель медитации"""

    name = models.CharField(
        _('Название'),
        max_length=100
    )
    file = models.FileField(
        _('Аудиофайл(mp3)'),
        upload_to='meditations/',
    )
    text = models.TextField(
        _('Текст'),
        max_length=1000
    )
