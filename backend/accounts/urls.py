from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.viewsets.auth_viewset import RegisterViewSet, LoginViewSet, LogoutViewSet
from accounts.viewsets.profile_viewset import ProfileViewSet, UserSearchViewSet
from accounts.viewsets.follow_viewset import FollowViewSet

router = DefaultRouter()

# Authentication routes
router.register(r'auth/register', RegisterViewSet, basename='register')
router.register(r'auth/login', LoginViewSet, basename='login')
router.register(r'auth', LogoutViewSet, basename='logout')

# Profile routes
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'search', UserSearchViewSet, basename='user-search')

# Follow routes
router.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('', include(router.urls)),
]
