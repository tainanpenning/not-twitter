from django.db.models import Count

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from accounts.models.profile import Profile
from accounts.serializers.profile_serializer import ProfileSerializer, ProfileUpdateSerializer, UserSearchSerializer
from accounts.permissions import IsOwnerOrReadOnly


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'user__username'

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
        if self.kwargs.get('user__username') == 'me':
            self.kwargs['user__username'] = self.request.user.username
        return super().get_object()

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user != self.request.user:
            return Response({'detail': 'Not authorized to update this profile.'}, status=status.HTTP_403_FORBIDDEN)
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
