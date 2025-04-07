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
    file_id = models.CharField(
        _('File id'),
        max_length=150,
        default=None,
        null=True,
        blank=True
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


class Review(AsyncBaseModel):
    """Модель отзыва медитации"""

    text = models.TextField(_('Текст'))
    meditation = models.ForeignKey(
        'meditations.Meditation',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('Медитация')
    )
    telegram_user = models.ForeignKey(
        'telegram_users.TelegramUser',
        on_delete=models.SET_NULL,
        related_name='reviews',
        verbose_name=_('Пользователь'),
        null=True,
    )

    class Meta:
        verbose_name = _('Отзыв медитации')
        verbose_name_plural = _('Отзывы медитаций')

    def __str__(self):
        return self.text[:100]