from django.contrib import admin
from .models import *

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ["id", "tid", "title"]
    

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ["id"]
    
    
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "correct"]
    
@admin.register(UserAnswer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["user", "test", "question", "answer", "check_answer"]
    list_filter = ["user", "test"]