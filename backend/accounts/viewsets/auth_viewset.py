from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from accounts.serializers.auth_serializer import RegisterSerializer, LoginSerializer


class RegisterViewSet(viewsets.ViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    throttle_scope = "auth_register"

    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class LoginViewSet(viewsets.ViewSet):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    throttle_scope = "auth_login"

    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                },
            },
            status=status.HTTP_200_OK,
        )


class TokenRefreshViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        refresh = request.data.get("refresh")

        if not refresh:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh_token = RefreshToken(refresh)
            access = str(refresh_token.access_token)

            return Response(
                {
                    "access": access,
                    "refresh": refresh,
                },
                status=status.HTTP_200_OK,
            )
        except (InvalidToken, TokenError):
            return Response({"detail": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        refresh_token = request.data.get("refresh")

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            pass

        return Response({"detail": "Logged out"}, status=200)
