from django.urls import path

from posts.viewsets.feed_viewset import FeedAPIView

urlpatterns = [
    path('', FeedAPIView.as_view(), name='feed'),
]
