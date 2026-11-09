from django.contrib import admin
from .models import ChatSession, ChatMessage


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'title')
    inlines = [ChatMessageInline]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'message_preview', 'response_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('message', 'response', 'session__user__username')

    def message_preview(self, obj):
        if obj.message:
            return obj.message[:40] + ("..." if len(obj.message) > 40 else "")
        return ""
    message_preview.short_description = "User Message"

    def response_preview(self, obj):
        if obj.response:
            return obj.response[:40] + ("..." if len(obj.response) > 40 else "")
        return ""
    response_preview.short_description = "Bot Response"
