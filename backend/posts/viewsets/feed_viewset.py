from django.db.models import Count, Exists, OuterRef
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from posts.serializers.post_serializer import PostSerializer
from posts.models.like import Like
from posts.models.post import Post


class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return (
            Post.objects.filter(
                is_active=True,
                author__in=user.following.values_list('following', flat=True),
            )
            .select_related('author', 'author__profile')
            .annotate(
                _likes_count=Count('likes'),
                _comments_count=Count('comments'),
                _is_liked=(
                    Exists(
                        Like.objects.filter(post_id=OuterRef('pk'), user=user),
                    )
                ),
            )
            .order_by('-created_at')
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
