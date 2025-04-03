from django.db import models
from django.utils.translation import gettext_lazy as _

from web.db.model_mixins import (
    AsyncBaseModel,
    SingletonModelMixin,
)
from web.validators.file import FileValidator


class BotMessages(AsyncBaseModel, SingletonModelMixin):
    """Singleton модель сообщений бота"""

    welcome_video = models.FileField(
        _('Приветственное видео'),
        upload_to='bot_media/',
        validators=[FileValidator(
            allowed_extensions=('.mp4', )
        )],
    )
    enter_info_text = models.TextField(
        _('Текст "Вводная информация"'),
        max_length=4000,
    )
    about_teacher_video = models.FileField(
        _('Видео об учителе'),
        validators=[
            FileValidator(allowed_extensions=('.mp4',))
        ]
    )
    about_teacher_text = models.TextField(
        _('Текст об учителе'),
        max_length=4000,
    )
    useful_posts_text = models.TextField(
        _('Текст полезные статьи'),
        max_length=4000,
    )
    society_video = models.FileField(
        _('Видео сообщества'),
        validators=[
            FileValidator(allowed_extensions=('.mp4', ))
        ]
    )
    faq_text = models.TextField(
        _('Текст ответы на вопросы'),
        max_length=4000,
    )
    reviews_file_1 = models.FileField(
        _('Видео/Фото отзывов 1'),
        validators=[
            FileValidator(allowed_extensions=('.mp4', '.jpg', '.jpeg', '.png'))
        ]
    )
    reviews_file_2 = models.FileField(
        _('Видео/Фото отзывов 2'),
        validators=[
            FileValidator(allowed_extensions=('.mp4', '.jpg', '.jpeg', '.png'))
        ]
    )
    reviews_file_3 = models.FileField(
        _('Видео/Фото отзывов 3'),
        validators=[
            FileValidator(allowed_extensions=('.mp4', '.jpg', '.jpeg', '.png'))
        ]
    )
    reviews_file_4 = models.FileField(
        _('Видео/Фото отзывов 4'),
        validators=[
            FileValidator(allowed_extensions=('.mp4', '.jpg', '.jpeg', '.png'))
        ]
    )
    reviews_text = models.TextField(
        _('Текст отзывы'),
        max_length=4000,
    )

    class Meta:
        verbose_name = _('Сообщения бота')
        verbose_name_plural = verbose_name

    def __str__(self):
        return ''


class Links(AsyncBaseModel, SingletonModelMixin):
    """Singleton модель ссылок"""

    channel_link = models.URLField(_('Ссылка на канал'))
    manager_link = models.URLField(_('Ссылка на аккаунт менеджера'))

    class Meta:
        verbose_name = _('Ссылки')
        verbose_name_plural = verbose_name

    def __str__(self):
        return ''