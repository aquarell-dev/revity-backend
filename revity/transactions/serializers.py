from rest_framework.serializers import ModelSerializer

from transactions.models import TransactionCategory, Transaction


class TransactionCategorySerializer(ModelSerializer):
    class Meta:
        model = TransactionCategory
        fields = "__all__"


class TransactionCreateSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "transaction_type",
            "amount",
            "category",
            "receiver",
            "transaction_date",
            "card",
        )


class TransactionRetrieveSerializer(ModelSerializer):
    category = TransactionCategorySerializer()

    class Meta:
        model = Transaction
        fields = "__all__"
