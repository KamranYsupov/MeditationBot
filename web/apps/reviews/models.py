from django.db import models
from django.utils.translation import gettext_lazy as _

from web.db.model_mixins import (
    AsyncBaseModel,
)


class Review(AsyncBaseModel):
    """Модель отзыва"""

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
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')

    def __str__(self):
        return self.text[:100]