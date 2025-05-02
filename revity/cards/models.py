from django.db import models
from django.db.models import Sum, Case, When, F
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib import admin

from transactions.models import Transaction, TransactionType


class Card(models.Model):
    PLACEHOLDER_DOTS = "•••• •••• •••• "

    user = models.ForeignKey(
        "users.CustomUser",
        verbose_name=_("Пользователь"),
        on_delete=models.CASCADE,
    )
    card_number = models.PositiveBigIntegerField(_("Номер карты"), unique=True)
    active_until = models.DateField(_("Активна до"))

    def __str__(self):
        return f"{self.protected_card_number} / {self.user.email}"

    @property
    @admin.display(boolean=True, description="Активна")
    def is_active(self):
        return self.active_until >= timezone.now().date()

    @property
    @admin.display(description="Номер карты")
    def protected_card_number(self):
        return self.PLACEHOLDER_DOTS + "".join(str(self.card_number)[-4:])

    @property
    @admin.display(description="Баланс")
    def balance(self):
        balance = (
            Transaction.objects.filter(card=self)
            .aggregate(
                balance=Sum(
                    Case(
                        When(
                            transaction_type=TransactionType.INCOME,
                            then=F("amount"),
                        ),
                        When(
                            transaction_type=TransactionType.EXPENSE,
                            then=-F("amount"),
                        ),
                        output_field=models.DecimalField(),
                    )
                ),
            )
            .get("balance")
        )

        return balance or 0

    class Meta:
        verbose_name = "Банковская карта"
        verbose_name_plural = "Банковские карты"
        constraints = [
            models.CheckConstraint(
                check=models.Q(card_number__gte=10**15, card_number__lte=10**16 - 1),
                name="card_number_16_digits",
            ),
        ]
