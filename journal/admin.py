from django.contrib import admin
from .models import Journal


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('username', 'date', 'content_preview')
    list_filter = ('date',)
    search_fields = ('username', 'content')

    def content_preview(self, obj):
        if obj.content:
            return obj.content[:50] + ("..." if len(obj.content) > 50 else "")
        return ""
    content_preview.short_description = "Content"
