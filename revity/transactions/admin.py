from django.contrib import admin

from transactions.models import TransactionCategory, Transaction


@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ("category",)
    list_filter = ("category",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_type",
        "amount",
        "category",
        "get_fixed_receiver",
        "transaction_date",
    )
    list_display_links = ("transaction_type", "amount")
    list_filter = ("transaction_type", "category")

    def get_fixed_receiver(self, obj):
        return obj.receiver or "Пользователь"

    get_fixed_receiver.short_description = "Получатель"
