from django.urls import path

from accounts.viewsets.profile_viewset import (
    ProfileListAPIView,
    ProfileDetailAPIView,
    MeAPIView,
)

urlpatterns = [
    path("", ProfileListAPIView.as_view()),
    path("me/", MeAPIView.as_view()),
    path("<str:username>/", ProfileDetailAPIView.as_view()),
]
