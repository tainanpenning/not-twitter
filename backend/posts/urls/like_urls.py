from django.urls import path

from posts.viewsets.like_viewset import LikeAPIView

urlpatterns = [
    path('<int:post_id>/like/', LikeAPIView.as_view(), name='post-like'),
]
