import pytest
import uuid
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from accounts.models.profile import Profile
from accounts.models.follow import Follow


@pytest.fixture
def api_client():
    """Returns an APIClient for testing."""
    return APIClient()


@pytest.fixture
def user_factory():
    """Factory to create users for testing."""

    def create_user(username=None, email=None, password='testpass123'):
        if not username:
            username = f'user_{uuid.uuid4().hex[:8]}'
        if not email:
            email = f'{username}@example.com'

        user = User.objects.create_user(username=username, email=email, password=password)
        return user

    return create_user


@pytest.fixture
def authenticated_client(api_client, user_factory):
    """Client authenticated with a test user."""
    user = user_factory()
    token = Token.objects.create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return api_client, user, token


@pytest.fixture
def profile_factory(user_factory):
    """Factory to create profiles with users."""

    def create_profile(display_name='Test User', bio='Test bio', username=None):
        if not username:
            username = f'user_{uuid.uuid4().hex[:8]}'
        user = user_factory(username=username)
        profile = Profile.objects.get(user=user)  # Create profile via signal
        profile.display_name = display_name
        profile.bio = bio
        profile.save()
        return profile

    return create_profile


@pytest.fixture
def two_users(user_factory):
    """Fixture with two users."""
    user1 = user_factory(username='user1', email='user1@example.com')
    user2 = user_factory(username='user2', email='user2@example.com')
    return user1, user2


@pytest.fixture
def follow_factory(two_users):
    """Factory to create follow relationships."""
    user1, user2 = two_users

    def create_follow(follower=user1, following=user2):
        follow = Follow.objects.create(follower=follower, following=following)
        return follow

    return create_follow
