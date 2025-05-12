from rest_framework import routers

from transactions.views import TransactionsViewSet

router = routers.SimpleRouter()
router.register(r"api/v1/users/me/transactions", TransactionsViewSet, basename="transactions")

urlpatterns = router.urls
