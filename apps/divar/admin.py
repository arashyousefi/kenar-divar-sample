from django.contrib import admin

from apps.divar.models import TempAuthorizationData, Chat, ChatMessage, Landing


@admin.register(TempAuthorizationData)
class TempAuthorizationDataAdmin(admin.ModelAdmin):
    list_display = ["user", "scope"]


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    readonly_fields = ["created_at", "message_text"]
    fields = ["id", "created_at", "message_text"]

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

    list_display = ["uuid", "post_token"]
    inlines = [ChatMessageInline]


@admin.register(Landing)
class LandingAdmin(admin.ModelAdmin):
    pass