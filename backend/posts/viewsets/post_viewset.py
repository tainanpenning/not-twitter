from django.db.models import (
    Count,
    Exists,
    OuterRef,
    BooleanField,
    Value,
)

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from posts.models.post import Post
from posts.models.like import Like
from posts.serializers.post_serializer import PostSerializer, PostWriteSerializer
from posts.permissions import IsPostAuthorOrReadOnly
from posts.pagination import PostPagination
from posts.services.post_service import PostService


class PostViewSet(viewsets.ModelViewSet):
    pagination_class = PostPagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsPostAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostWriteSerializer

        return PostSerializer

    def get_queryset(self):
        queryset = (
            Post.objects.filter(is_active=True)
            .select_related('author', 'author__profile')
            .annotate(
                _likes_count=Count('likes', distinct=True),
                _comments_count=Count('comments', distinct=True),
            )
        )

        if self.request.user.is_authenticated:
            queryset = queryset.annotate(
                _is_liked=Exists(
                    Like.objects.filter(
                        post_id=OuterRef('pk'),
                        user=self.request.user,
                    )
                )
            )

        else:
            queryset = queryset.annotate(
                _is_liked=Value(
                    False,
                    output_field=BooleanField(),
                )
            )

        author = self.request.query_params.get('author')

        if author:
            queryset = queryset.filter(author__username=author)

        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        PostService.soft_delete_post(instance)
