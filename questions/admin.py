from django.contrib import admin
from .models import Question, Tag, TagCategory

class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_filter = ('approved', 'answered', 'published', 'answered_by')
    list_display = ('question', 'email', 'created_at', 'approved', 'answered', 'published')
    date_hierarchy = 'created_at'
    search_fields = ('question', 'edited_question', 'answer', 'email')
    fields = (
        ('email', 'created_at', 'changed_at'),
        'question',
        'approved',
        'edited_question',
        'answer',
        'answered_by',
        'tags',
        ('answered', 'answered_at'),
        ('published', 'published_at'),
        
    )
    readonly_fields = ['created_at', 'answered_at', 'published_at', 'changed_at']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Tag)
admin.site.register(TagCategory)
