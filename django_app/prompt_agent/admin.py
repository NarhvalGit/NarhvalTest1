"""Admin configuration for the prompt agent."""
from django.contrib import admin
from .models import AgentSession, PromptResponse


@admin.register(AgentSession)
class AgentSessionAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'is_active', 'created_at']
    list_filter = ['is_active', 'model', 'created_at']
    search_fields = ['name', 'system_prompt']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'model', 'is_active')
        }),
        ('Configuration', {
            'fields': ('system_prompt',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PromptResponse)
class PromptResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_prompt_preview', 'session', 'status', 'model_used', 'created_at', 'processing_time']
    list_filter = ['status', 'model_used', 'created_at']
    search_fields = ['prompt', 'response']
    readonly_fields = ['created_at', 'updated_at', 'processing_time']

    fieldsets = (
        ('Session', {
            'fields': ('session',)
        }),
        ('Content', {
            'fields': ('prompt', 'response')
        }),
        ('Status', {
            'fields': ('status', 'error_message')
        }),
        ('Metadata', {
            'fields': ('model_used', 'processing_time', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_prompt_preview(self, obj):
        return obj.prompt[:50] + '...' if len(obj.prompt) > 50 else obj.prompt
    get_prompt_preview.short_description = 'Prompt'
