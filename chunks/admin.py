from django.contrib import admin
from fnpdjango.utils.models.translation import translated_fields
from .models import Chunk, Attachment


class ChunkAdmin(admin.ModelAdmin):
    list_display = ('key', 'description',)
    search_fields = ('key', ) + translated_fields(('content',))

admin.site.register(Chunk, ChunkAdmin)


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('key',)
    search_fields = ('key',)

admin.site.register(Attachment, AttachmentAdmin)