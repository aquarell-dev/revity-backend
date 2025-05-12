from rest_framework.serializers import ModelSerializer

from goals.models import Goal


class GoalListDetailSerializer(ModelSerializer):
    class Meta:
        model = Goal
        fields = ("id", "goal_name", "approximate_cost", "execution_date")


class GoalCreateSerializer(ModelSerializer):
    class Meta:
        model = Goal
        fields = ("goal_name", "approximate_cost", "execution_date")
