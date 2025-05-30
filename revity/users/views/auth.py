from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from users.models import CustomUser
from users.serializers import RegisterSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = CustomUser.objects.create_user(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        refresh = RefreshToken.for_user(user)

        response = Response(
            {
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )

        response.set_cookie(
            key=settings.REFRESH_TOKEN_COOKIE_NAME,
            value=str(refresh),
            httponly=True,
            secure=not settings.DEBUG,
            samesite="None",
            path="/",
        )

        return response


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response({"detail": "Неправильные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        response = Response(
            {
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
            key=settings.REFRESH_TOKEN_COOKIE_NAME,
            value=str(refresh),
            httponly=True,
            secure=not settings.DEBUG,
            samesite="None",
            path="/",
        )

        return response


class CookieTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(settings.REFRESH_TOKEN_COOKIE_NAME)

        if refresh_token is None:
            raise AuthenticationFailed("Refresh token not found in cookie")

        request.data["refresh"] = refresh_token

        try:
            response = super().post(request, *args, **kwargs)
        except TokenError as e:
            response = Response({"detail": "Refresh token expired or invalid"}, status=401)
            response.delete_cookie(settings.REFRESH_TOKEN_COOKIE_NAME)
            return response

        # Remove refresh token from the response body
        access_token = response.data.get("access")
        refresh_token = response.data.get("refresh")
        response.data.clear()
        response.data["access"] = access_token

        # Set new refresh token in cookie if present
        if refresh_token:
            response.set_cookie(
                key=settings.REFRESH_TOKEN_COOKIE_NAME,
                value=refresh_token,
                httponly=True,
                secure=not settings.DEBUG,
                samesite="None",
                path="/",
            )

        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response({"detail": "Logged out"}, status=status.HTTP_200_OK)
        response.delete_cookie(settings.REFRESH_TOKEN_COOKIE_NAME)
        return response
