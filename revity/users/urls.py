from django.urls import path
from .views.auth import LoginView, CookieTokenRefreshView, LogoutView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
