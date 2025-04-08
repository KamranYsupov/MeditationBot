from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from web.admin.mixins import SingletonModelAdmin
from .models import Links, BotMessages, BotReview


@admin.register(BotMessages)
class BotMessagesAdmin(SingletonModelAdmin):
    fieldsets = (
        (_('Приветствие'), {
            'fields': ('welcome_video', 'welcome_text')
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
    )


@admin.register(Links)
class LinksAdmin(SingletonModelAdmin):
    pass


@admin.register(BotReview)
class BotReviewAdmin(admin.ModelAdmin):
    pass
