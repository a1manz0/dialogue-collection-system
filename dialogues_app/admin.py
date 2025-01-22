from django.contrib import admin
from .models import ClientQuestion

@admin.register(ClientQuestion)
class ClientQuestionAdmin(admin.ModelAdmin):
    list_display = ('topic', 'complexity', 'requires_crm', 'created_by', 'created_at')
    list_filter = ('topic', 'complexity', 'requires_crm', 'created_at')
    search_fields = ('question', 'answer', 'tags')
    date_hierarchy = 'created_at' 