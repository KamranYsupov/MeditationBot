from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from asgiref.sync import sync_to_async

from web.db.model_mixins import (
    AsyncBaseModel,
    OrderMixin
)
from web.validators.file import FileValidator


class Topic(AsyncBaseModel, OrderMixin):
    """Модель темы"""

    TECHNOLOGY = 'Tech'
    POST = 'Post'

    TYPE_CHOICES = (
        (TECHNOLOGY, 'О технологии'),
        (POST, 'Полезная информация')
    )

    name = models.CharField(
        _('Название'),
        max_length=100,
        unique=True
    )
    link = models.URLField(
        _('Ссылка'),
        max_length=200,
        default='https://google.com',
    )
    type = models.CharField(
        _('Раздел'),
        choices=TYPE_CHOICES,
        max_length=30,
        default=TECHNOLOGY,
    )

    class Meta:
        verbose_name = _('О технологии / Полезная информация')
        verbose_name_plural = _('О технологии / Полезная информация')
        ordering = ['order']

    def __str__(self):
        return self.name


class Question(AsyncBaseModel, OrderMixin):
    """Модель вопроса"""

    title = models.CharField(
        _('Заголовок'),
        max_length=100,
        unique=True
    )
    video = models.FileField(
        _('Видео(mp4)'),
        validators=[
            FileValidator(allowed_extensions=('.mp4', ))
        ],
        null=True,
        blank=True,
        default=None,
    )
    photo = models.FileField(
        _('Фото(.jpg/.jpeg/.png)'),
        validators=[
            FileValidator(allowed_extensions=('.jpg', '.jpeg', '.png'))
        ],
        null=True,
        blank=True,
        default=None,
    )

    text = models.TextField(
        _('Текст'),
        null=True,
        blank=True,
        default=None,
    )

    class Meta:
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')
        ordering = ['order']

    def __str__(self):
        return self.title


    def clean(self):
        super().clean()

        if not self.video and not self.photo and not self.text:
            raise ValidationError('Текст, фото или видео должно быть добавлено')

        if not self.text:
            return

        if (self.video or self.photo) and len(self.text) > 1000:
            raise ValidationError(
                'При добавлении медиафайла длина текста на должна превышать 1000 символов'
            )

        if len(self.text) > 4000:
            raise ValidationError('Длина текста на должна превышать 4000 символов')

