from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from web.admin.mixins import SingletonModelAdmin
from .models import Links, BotMessages


@admin.register(BotMessages)
class BotMessagesAdmin(SingletonModelAdmin):
    fieldsets = (
        (_('Приветствие'), {
            'fields': ('welcome_video',)
        }),
        (_('Медитации'), {
            'fields': ('enter_info_text',),
        }),
        (_('Об учителе'), {
            'fields': ('about_teacher_video', 'about_teacher_text'),
            'description': _('Раздел с информацией о преподавателе')
        }),
        (_('Полезные материалы'), {
            'fields': ('useful_posts_text',)
        }),
        (_('Сообщество'), {
            'fields': ('society_video',)
        }),
        (_('FAQ'), {
            'fields': ('faq_text',)
        }),
        (_('Отзывы'), {
            'fields': (
                'reviews_file_1',
                'reviews_file_2',
                'reviews_file_3',
                'reviews_file_4',
                'reviews_text'
            ),
            'description': _('Медиафайлы и текстовые отзывы')
        }),
    )


@admin.register(Links)
class LinksAdmin(SingletonModelAdmin):
    pass

