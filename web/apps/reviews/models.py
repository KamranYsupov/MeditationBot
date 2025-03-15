from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from asgiref.sync import sync_to_async

from web.db.model_mixins import (
    AsyncBaseModel,
)


class Review(AsyncBaseModel):
    """Модель отзыва"""

    text = models.TextField(_('Текст'))
    meditation = models.ForeignKey(
        'meditations.Meditation',
        on_delete=models.CASCADE,
        related_name='reviews'
    )