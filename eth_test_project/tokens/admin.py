from django.contrib import admin

from .models import Token


@admin.register(Token)
class ToolAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'tx_hash', 'owner',
    )
