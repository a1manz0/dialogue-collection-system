from django.contrib import admin
from .models import Dialogue, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0

@admin.register(Dialogue)
class DialogueAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'requires_crm', 'created_by', 'created_at')
    list_filter = ('topic', 'requires_crm', 'created_at')
    search_fields = ('topic', 'created_by__username')
    inlines = [MessageInline]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'dialogue', 'author', 'text', 'created_at')
    list_filter = ('author', 'created_at')
    search_fields = ('text',) 