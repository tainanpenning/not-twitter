from django.db.models import Count, Exists, OuterRef
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied

from posts.models.post import Post
from posts.models.like import Like
from posts.serializers.post_serializer import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = (
            Post.objects.filter(is_active=True)
            .select_related('author', 'author__profile')
            .annotate(
                _likes_count=Count('likes', distinct=True),
                _comments_count=Count('comments', distinct=True),
            )
            .order_by('-created_at')
        )
        if self.request.user.is_authenticated:
            queryset = queryset.annotate(
                is_liked=Exists(
                    Like.objects.filter(post_id=OuterRef('pk'), user=self.request.user),
                )
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied('You are not authorized to update this post.')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('You are not authorized to delete this post.')
        instance.is_active = False
        instance.save()
        instance.comments.update(is_active=False)
