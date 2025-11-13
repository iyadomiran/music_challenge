from django.contrib import admin
from .models import Challenge

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'correct', 'user_answer', 'created_at')
    list_filter = ('level', 'created_at')
    search_fields = ('user__username', 'correct', 'user_answer')