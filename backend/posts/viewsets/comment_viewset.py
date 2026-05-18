from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from posts.models.comment import Comment
from posts.models.post import Post

from posts.serializers.comment_serializer import CommentSerializer

from posts.permissions import IsCommentAuthorOrPostAuthor

from posts.pagination import CommentPagination


class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CommentPagination

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")

        return (
            Comment.objects.filter(
                post_id=post_id,
                is_active=True,
            )
            .select_related(
                'author',
                'author__profile',
            )
            .order_by('-created_at')
        )

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")

        post = get_object_or_404(
            Post,
            pk=post_id,
        )

        serializer.save(
            author=self.request.user,
            post=post,
        )


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthorOrPostAuthor]

    queryset = Comment.objects.select_related(
        'author',
        'author__profile',
    )

    def perform_update(self, serializer):
        comment = self.get_object()

        if comment.author != self.request.user:
            raise PermissionDenied(("Not authorized " "to update this comment."))

        serializer.save()

    def perform_destroy(self, instance):
        is_comment_author = instance.author == self.request.user
        is_post_author = instance.post.author == self.request.user

        if not (is_comment_author or is_post_author):
            raise PermissionDenied(("Not authorized " "to delete this comment."))

        instance.delete()
