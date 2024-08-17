from django.contrib import admin

from apps.divar.models import TempAuthorizationData, Chat


@admin.register(TempAuthorizationData)
class TempAuthorizationDataAdmin(admin.ModelAdmin):
    list_display = ["user"]


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    pass