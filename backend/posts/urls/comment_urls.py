from django.urls import path

from posts.viewsets.comment_viewset import (
    CommentListCreateAPIView,
    CommentDetailAPIView,
)

urlpatterns = [
    path('<int:post_id>/comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'),
]
