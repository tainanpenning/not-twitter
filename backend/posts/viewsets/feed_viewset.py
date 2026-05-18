from django.db.models import Count, Exists, OuterRef

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from posts.models.like import Like
from posts.models.post import Post
from posts.serializers.post_serializer import PostSerializer
from posts.pagination import FeedPagination


class FeedAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = FeedPagination

    def get_queryset(self):
        user = self.request.user
        following_ids = user.following.values_list('following', flat=True)

        return (
            Post.objects.filter(
                is_active=True,
                author__in=following_ids,
            )
            .select_related(
                'author',
                'author__profile',
            )
            .annotate(
                _likes_count=Count(
                    'likes',
                    distinct=True,
                ),
                _comments_count=Count(
                    'comments',
                    distinct=True,
                ),
                _is_liked=Exists(
                    Like.objects.filter(
                        post_id=OuterRef('pk'),
                        user=user,
                    )
                ),
            )
            .order_by('-created_at')
        )
