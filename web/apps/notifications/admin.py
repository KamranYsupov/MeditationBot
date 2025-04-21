from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    filter_horizontal = ('receivers',)

    def has_change_permission(self, request, obj=None):
        return False