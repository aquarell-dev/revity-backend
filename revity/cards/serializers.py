from rest_framework.serializers import ModelSerializer

from cards.models import Card


class CardListDetailSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ("id", "protected_card_number", "active_until", "balance")


class CardCreateSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ("card_number", "active_until")
