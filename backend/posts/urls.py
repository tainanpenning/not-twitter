from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts.viewsets.post_viewset import PostViewSet
from posts.viewsets.comment_viewset import CommentViewSet
from posts.viewsets.like_viewset import LikeViewSet
from posts.viewsets.feed_viewset import FeedViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'likes', LikeViewSet, basename='like')
router.register(r'feed', FeedViewSet, basename='feed')

urlpatterns = [
    path('', include(router.urls)),
]
