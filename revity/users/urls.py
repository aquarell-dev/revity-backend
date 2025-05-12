from django.urls import path
from .views.auth import LoginView, CookieTokenRefreshView, LogoutView, RegisterView
from .views.users import MeView

urlpatterns = [
    path(r"auth/sign-in/", LoginView.as_view(), name="login"),
    path(r"auth/sign-out/", LogoutView.as_view(), name="logout"),
    path(r"auth/sign-up/", RegisterView.as_view(), name="logout"),
    path(r"auth/token/refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
    path(r"users/me/", MeView.as_view(), name="users"),
]
