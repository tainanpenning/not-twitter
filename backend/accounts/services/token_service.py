from rest_framework_simplejwt.tokens import RefreshToken


class AuthService:

    @staticmethod
    def build_auth_response(user):
        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
            },
        }
