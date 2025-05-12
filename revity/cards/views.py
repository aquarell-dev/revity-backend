from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from cards.models import Card
from cards.serializers import CardListDetailSerializer, CardCreateSerializer


class CardViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user).order_by("-id")

    def get_serializer(self, *args, **kwargs):
        if self.request.method == "GET":
            return CardListDetailSerializer(*args, **kwargs)

        return CardCreateSerializer(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
