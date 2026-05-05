from rest_framework import viewsets, status
from rest_framework.response import Response

from posts.models.comment import Comment
from posts.serializers.comment_serializer import CommentSerializer
from posts.permissions import IsCommentAuthorOrPostAuthor


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthorOrPostAuthor]

    def get_queryset(self):
        queryset = Comment.objects.filter(
            is_active=True,
        ).select_related('author', 'author__profile')
        post_id = self.request.query_params.get('post_id')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.author != self.request.user:
            return Response({'detail': 'Not authorized to update this comment.'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()

    def perform_destroy(self, instance):
        post_author = instance.post.author
        if instance.author != self.request.user and post_author != self.request.user:
            return Response({'detail': 'Not authorized to delete this comment.'}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()
