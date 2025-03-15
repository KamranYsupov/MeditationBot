from django.contrib import admin

from .models import Meditation


@admin.register(Meditation)
class MeditationAdmin(admin.ModelAdmin):
    pass