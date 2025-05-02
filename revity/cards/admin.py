from django.contrib import admin

from cards.models import Card


PLACEHOLDER_DOTS = "•••• •••• •••• "


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("protected_card_number", "balance", "is_active")
    list_display_links = ("protected_card_number",)
    readonly_fields = ("balance",)
