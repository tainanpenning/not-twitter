from django.urls import path

from accounts.viewsets.follow_viewset import (
    FollowAPIView,
    FollowersAPIView,
    FollowingAPIView,
)

urlpatterns = [
    path("<str:username>/follow/", FollowAPIView.as_view(), name="follow-toggle"),
    path("<str:username>/followers/", FollowersAPIView.as_view(), name="followers-list"),
    path("<str:username>/following/", FollowingAPIView.as_view(), name="following-list"),
]
