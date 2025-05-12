from rest_framework import routers

from goals.views import GoalViewSet

router = routers.SimpleRouter()
router.register(r"api/v1/users/me/goals", GoalViewSet, basename="goals")

urlpatterns = router.urls
