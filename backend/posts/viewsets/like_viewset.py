from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models.like import Like
from posts.models.post import Post


class LikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(
            Post,
            pk=post_id,
            is_active=True,
        )

        already_liked = Like.objects.filter(
            post=post,
            user=request.user,
        ).exists()

        if already_liked:
            return Response(
                {"detail": "Post already liked."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Like.objects.create(
            post=post,
            user=request.user,
        )

        return Response(
            {
                "liked": True,
                "likes_count": post.likes.count(),
            },
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, post_id):
        post = get_object_or_404(
            Post,
            pk=post_id,
            is_active=True,
        )

        like = Like.objects.filter(
            post=post,
            user=request.user,
        )

        if not like.exists():
            return Response(
                {"detail": "Like not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        like.delete()

        return Response(
            {
                "liked": False,
                "likes_count": post.likes.count(),
            },
            status=status.HTTP_200_OK,
        )
