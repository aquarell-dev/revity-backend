from django.http import Http404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import TransactionRetrieveSerializer, TransactionCreateSerializer
from .services import get_transactions, get_transactions_by_card


class TransactionsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_transactions(self.request.user)

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return TransactionRetrieveSerializer

        return TransactionCreateSerializer

    def perform_create(self, serializer):
        card = serializer.validated_data["card"]

        if card.user_id != self.request.user.id:
            raise Http404("Card not found")

        serializer.save()

    @action(
        detail=False,
        methods=["GET"],
        url_path="(?P<card_id>[^/.]+)",
    )
    def transactions_by_user(self, request, card_id=None):
        transactions = get_transactions_by_card(self.request.user, card_id=card_id)

        serializer = self.get_serializer(transactions, many=True)

        return Response(serializer.data)
