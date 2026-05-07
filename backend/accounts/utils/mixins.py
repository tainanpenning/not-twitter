from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class MeUserMixin:
    def get_user_from_param(self, request, username: str):
        if username == "me":
            return request.user
        return get_object_or_404(User, username=username)
