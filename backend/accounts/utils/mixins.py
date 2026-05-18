from django.db.models import Count
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from accounts.models.profile import Profile


class BaseProfileQuerysetMixin:
    def get_queryset(self):
        return Profile.objects.select_related('user').annotate(
            _followers_count=Count(
                'user__followers',
                distinct=True,
            ),
            _following_count=Count(
                'user__following',
                distinct=True,
            ),
        )


class MeUserMixin:
    def get_user_from_param(self, request, username: str):
        if username == "me":
            return request.user
        return get_object_or_404(User, username=username)
