from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False