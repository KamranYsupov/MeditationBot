from django.contrib import admin

from .models import Topic, Question


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'type')


    list_filter = ('type', )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass