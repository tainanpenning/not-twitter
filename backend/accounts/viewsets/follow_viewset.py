from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from accounts.models.follow import Follow
from accounts.serializers.profile_serializer import UserSearchSerializer


class FollowPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class FollowViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = FollowPagination
    throttle_scope = "follow"

    def _paginate(self, queryset, request):
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = UserSearchSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(detail=False, methods=['post'], url_path='toggle/(?P<username>[^/.]+)')
    def toggle(self, request, username=None, **kwargs):
        target_user = get_object_or_404(User, username=username)

        if request.user == target_user:
            return Response(
                {'detail': "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target_user,
        )

        if not created:
            follow.delete()
            return Response(
                {'detail': 'Unfollowed successfully.'},
                status=status.HTTP_200_OK,
            )
        return Response(
            {'detail': 'Followed successfully.'},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=['get'], url_path='followers/(?P<username>[^/.]+)')
    def followers_list(self, request, username=None, **kwargs):
        target_user = get_object_or_404(User, username=username)
        follower_users = (
            User.objects.filter(
                following__following=target_user,
            )
            .select_related('profile')
            .order_by('username'),
        )
        return self._paginate(follower_users, request)

    @action(detail=False, methods=['get'], url_path='following/(?P<username>[^/.]+)')
    def following_list(self, request, username=None, **kwargs):
        target_user = get_object_or_404(User, username=username)
        following_users = (
            User.objects.filter(
                followers__follower=target_user,
            )
            .select_related('profile')
            .order_by('username'),
        )
        return self._paginate(following_users, request)
