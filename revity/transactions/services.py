from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import Sum, Case, When, F, DecimalField

from transactions.models import Transaction, TransactionType


def get_transactions(user: AbstractBaseUser):
    return (
        Transaction.objects.filter(card__user=user)
        .select_related("user")
        .order_by("-transaction_date")
    )


def get_transactions_by_card(user: AbstractBaseUser, *, card_id: int):
    return (
        Transaction.objects.filter(card__user=user, card__id=card_id)
        .select_related("user")
        .order_by("-transaction_date")
    )


def _get_balance(**kwargs):
    balance = (
        Transaction.objects.filter(**kwargs)
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
                    output_field=DecimalField(),
                )
            ),
        )
        .get("balance")
    )

    return balance or 0


def get_user_balance(user):
    return _get_balance(card__user=user)


def get_card_balance(card):
    return _get_balance(card=card)
