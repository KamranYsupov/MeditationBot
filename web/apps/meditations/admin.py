from django.contrib import admin

from .models import Meditation, Review

from django.contrib import admin


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(Meditation)
class MeditationAdmin(admin.ModelAdmin):


    exclude = ('file_id', )