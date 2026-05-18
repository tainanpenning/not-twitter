from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.models.profile import Profile
from accounts.serializers.profile_serializer import (
    ProfileSerializer,
    ProfileUpdateSerializer,
    UserSearchSerializer,
)
from accounts.permissions import IsOwnerOrReadOnly
from accounts.utils.mixins import BaseProfileQuerysetMixin


class ProfileListAPIView(BaseProfileQuerysetMixin, generics.ListAPIView):
    serializer_class = UserSearchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        queryset = super().get_queryset()

        if query:
            queryset = queryset.filter(
                Q(user__username__istartswith=query) | Q(display_name__icontains=query),
            )

        if not query:
            return queryset.none()

        return queryset.order_by('-created_at')


class ProfileDetailAPIView(BaseProfileQuerysetMixin, generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    lookup_url_kwarg = 'username'

    def get_object(self):
        username = self.kwargs.get('username')

        return get_object_or_404(
            self.get_queryset(),
            user__username=username,
        )


class MeAPIView(BaseProfileQuerysetMixin, generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)

        return profile

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return ProfileUpdateSerializer

        return ProfileSerializer
