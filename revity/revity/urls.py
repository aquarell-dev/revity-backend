from django.contrib import admin
from django.urls import path, include

from cards.urls import router as cards_router
from goals.urls import router as goals_router
from transactions.urls import router as transactions_router

urlpatterns = [
    path("admin/", admin.site.urls),
    path(r"api/v1/", include("users.urls")),
]

urlpatterns += transactions_router.urls
urlpatterns += cards_router.urls
urlpatterns += goals_router.urls
