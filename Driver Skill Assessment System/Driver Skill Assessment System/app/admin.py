# app/admin.py
from django.contrib import admin
from .models import Chapter, Question, QuizResult

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'description')
    search_fields = ('title', 'description')
    ordering = ('number',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'chapter', 'correct_option')
    search_fields = ('text',)
    list_filter = ('chapter',)
    ordering = ('chapter',)

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'quiz_date')
    search_fields = ('user__username', 'score')
    ordering = ('-quiz_date',)
