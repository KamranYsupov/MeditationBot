from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from asgiref.sync import sync_to_async

from web.db.model_mixins import (
    AsyncBaseModel,
)
from web.validators.file import FileValidator


class Meditation(AsyncBaseModel):
    """Модель медитации"""

    name = models.CharField(
        _('Название'),
        max_length=100,
        unique=True
    )
    file = models.FileField(
        _('Видеофайл(mp4)'),
        upload_to='meditations/',
        validators=[FileValidator(allowed_extensions=('.mp4', ))]
    )
    text = models.TextField(
        _('Текст'),
        max_length=1000
    )

    class Meta:
        verbose_name = _('Медитация')
        verbose_name_plural = _('Медитации')

    def __str__(self):
        return self.name
