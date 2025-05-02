from django.contrib import admin

from goals.models import Goal


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("goal_name", "approximate_cost", "execution_date")
    list_filter = ("goal_name",)
