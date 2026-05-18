from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models.profile import Profile
from accounts.models.follow import Follow
from accounts.serializers.profile_serializer import UserSearchSerializer
from accounts.utils.mixins import MeUserMixin
from accounts.pagination import FollowPagination


class BaseFollowAPIView(MeUserMixin):
    permission_classes = [IsAuthenticated]
    throttle_scope = "follow"

    def paginate_users(self, queryset, request):
        paginator = FollowPagination()

        page = paginator.paginate_queryset(queryset, request)

        serializer = UserSearchSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)


class FollowAPIView(BaseFollowAPIView, APIView):
    def post(self, request, username):
        target_user = self.get_user_from_param(request, username)

        if request.user == target_user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        follow_exists = Follow.objects.filter(
            follower=request.user,
            following=target_user,
        ).exists()

        if follow_exists:
            Follow.objects.filter(
                follower=request.user,
                following=target_user,
            ).delete()

            return Response(
                {"detail": "Unfollowed successfully."},
                status=status.HTTP_200_OK,
            )

        Follow.objects.create(
            follower=request.user,
            following=target_user,
        )

        return Response(
            {"detail": "Followed successfully."},
            status=status.HTTP_201_CREATED,
        )


class FollowersAPIView(BaseFollowAPIView, generics.ListAPIView):
    serializer_class = UserSearchSerializer

    def get_queryset(self):
        username = self.kwargs.get("username")

        target_user = self.get_user_from_param(
            self.request,
            username,
        )

        return (
            Profile.objects.filter(
                user__following__following=target_user,
            )
            .select_related('user')
            .order_by('user__username')
        )

    def list(self, request, *args, **kwargs):
        return self.paginate_users(
            self.get_queryset(),
            request,
        )


class FollowingAPIView(BaseFollowAPIView, generics.ListAPIView):
    serializer_class = UserSearchSerializer

    def get_queryset(self):
        username = self.kwargs.get("username")

        target_user = self.get_user_from_param(
            self.request,
            username,
        )

        return (
            Profile.objects.filter(
                user__followers__follower=target_user,
            )
            .select_related('user')
            .order_by('user__username')
        )

    def list(self, request, *args, **kwargs):
        return self.paginate_users(
            self.get_queryset(),
            request,
        )
