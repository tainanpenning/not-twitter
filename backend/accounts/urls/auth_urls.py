from django.urls import path

from accounts.viewsets.auth_viewset import (
    LoginAPIView,
    RegisterAPIView,
    LogoutAPIView,
    RefreshAPIView,
)

urlpatterns = [
    path("login/", LoginAPIView.as_view()),
    path("register/", RegisterAPIView.as_view()),
    path("logout/", LogoutAPIView.as_view()),
    path("refresh/", RefreshAPIView.as_view()),
]
