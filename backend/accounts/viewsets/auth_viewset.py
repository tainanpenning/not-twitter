from rest_framework.authtoken.models import Token

from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
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
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user_id": user.id, "username": user.username},
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
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user_id": user.id, "username": user.username},
            status=status.HTTP_200_OK,
        )


class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    throttle_scope = "auth_logout"

    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        return Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_200_OK,
        )
