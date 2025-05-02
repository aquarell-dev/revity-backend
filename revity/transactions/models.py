from django.db import models
from django.utils.translation import gettext_lazy as _


class TransactionType(models.TextChoices):
    INCOME = "IN", _("Поступление")
    EXPENSE = "EX", _("Трата")


class Transaction(models.Model):
    transaction_type = models.CharField(_("Тип транзакции"), choices=TransactionType.choices)
    amount = models.DecimalField(_("Сумма транзакции"), max_digits=18, decimal_places=2)
    category = models.ForeignKey(
        "transactions.TransactionCategory",
        verbose_name=_("Категория"),
        on_delete=models.CASCADE,
    )
    receiver = models.CharField(_("Получатель транзакции"), max_length=255, blank=True, null=True)
    transaction_date = models.DateTimeField(_("Дата транзакции"), auto_now=True)
    card = models.ForeignKey(
        "cards.Card",
        on_delete=models.CASCADE,
        verbose_name=_("Банковская карта"),
    )

    def __str__(self):
        return f"Транзакция на сумму {self.amount}₽ от {self.transaction_date.strftime("%d.%m.%Y %H:%M")}"

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"


class TransactionCategory(models.Model):
    category = models.CharField(_("Категория"), max_length=128)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "Категория транзакции"
        verbose_name_plural = "Категории транзакций"
