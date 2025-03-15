from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from asgiref.sync import sync_to_async

from web.db.model_mixins import (
    AsyncBaseModel,
    AbstractTelegramUser,
)


class TelegramUser(AbstractTelegramUser):
    """Модель telegram пользователя"""

    full_name = models.CharField(_('Имя'), max_length=200)
    phone_number = models.CharField(
        _('Номер телефона'),
        max_length=50,
        unique=True,
    )
    city = models.CharField(
        _('Город'),
        max_length=50,
        db_index=True,
    )
    time_joined = models.DateTimeField(
        _('Время добавления'),
        auto_now_add=True
    )

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('Telegram пользователи')
        ordering = ['-time_joined']

    def __str__(self):
        return self.full_name