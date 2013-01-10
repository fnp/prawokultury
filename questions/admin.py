from django.contrib import admin
from .models import Question

class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_filter = ('approved', 'answered', 'published')
    list_display = ('question', 'email', 'created_at', 'approved', 'answered', 'published')
    date_hierarchy = 'created_at'
    fields = (
        ('email', 'created_at'),
        'question',
        'approved',
        'edited_question',
        'answer',
        ('answered', 'answered_at'),
        ('published', 'published_at'),
        
    )
    readonly_fields = ['created_at', 'answered_at', 'published_at']


admin.site.register(Question, QuestionAdmin)
