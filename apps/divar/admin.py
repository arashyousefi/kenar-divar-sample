from django.contrib import admin

from apps.divar.models import TempAuthorizationData


@admin.register(TempAuthorizationData)
class TempAuthorizationDataAdmin(admin.ModelAdmin):
    list_display = ["user"]
