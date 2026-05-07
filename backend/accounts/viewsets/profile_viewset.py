from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from accounts.models.profile import Profile
from accounts.serializers.profile_serializer import ProfileSerializer, ProfileUpdateSerializer, UserSearchSerializer
from accounts.permissions import IsOwnerOrReadOnly


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'username'

    @action(detail=False, methods=["get", "patch"], permission_classes=[IsAuthenticated])
    def me(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)

        if request.method == "GET":
            serializer = self.get_serializer(profile)
            return Response(serializer.data)

        if request.method == "PATCH":
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    def get_queryset(self):
        return (
            Profile.objects.select_related('user')
            .annotate(
                _followers_count=Count(
                    'user__followers',
                    distinct=True,
                ),
                _following_count=Count('user__following', distinct=True),
            )
            .order_by('-created_at')
        )

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return ProfileUpdateSerializer
        return ProfileSerializer

    def get_object(self):
        username = self.kwargs.get(self.lookup_field)
        if username == 'me':
            username = self.request.user.username
        return get_object_or_404(
            self.get_queryset(),
            user__username=username,
        )

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied('Not authorized')
        serializer.save()


class UserSearchViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSearchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Profile.objects.select_related('user').annotate(
            _followers_count=Count('user__followers', distinct=True),
        )
        q = self.request.query_params.get('q', '')
        if q:
            queryset = queryset.filter(user__username__icontains=q)
        return queryset.order_by('user__username')
