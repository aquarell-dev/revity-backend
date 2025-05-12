from rest_framework import routers

from cards.views import CardViewSet

router = routers.SimpleRouter()
router.register(r"api/v1/users/me/cards", CardViewSet, basename="cards")

urlpatterns = router.urls
