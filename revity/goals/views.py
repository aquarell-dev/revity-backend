from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Goal
from .serializers import GoalListDetailSerializer, GoalCreateSerializer


class GoalViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user).order_by("-id")

    def get_serializer(self, *args, **kwargs):
        if self.request.method == "GET":
            return GoalListDetailSerializer(*args, **kwargs)

        return GoalCreateSerializer(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
