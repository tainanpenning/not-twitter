import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from posts.models.post import Post
from posts.models.comment import Comment
from posts.models.like import Like

_user_counter = 0


class UserFactory:
    """Factory for creating test users."""

    @staticmethod
    def create(username=None, email=None, password='testpass123'):
        """Create a new User with unique username and email."""
        global _user_counter
        _user_counter += 1

        if username is None:
            username = f'testuser{_user_counter}'
        if email is None:
            email = f'test{_user_counter}@example.com'

        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )


class PostFactory:
    """Factory for creating test posts."""

    @staticmethod
    def create(author=None, content='Test post content', media=None):
        """Create a new Post."""
        if author is None:
            author = UserFactory.create()

        return Post.objects.create(
            author=author,
            content=content,
            media=media,
        )


class CommentFactory:
    """Factory for creating test comments."""

    @staticmethod
    def create(post=None, author=None, content='Test comment'):
        """Create a new Comment."""
        if post is None:
            post = PostFactory.create()
        if author is None:
            author = UserFactory.create()

        return Comment.objects.create(
            post=post,
            author=author,
            content=content,
        )


class LikeFactory:
    """Factory for creating test likes."""

    @staticmethod
    def create(post=None, user=None):
        """Create a new Like."""
        if post is None:
            post = PostFactory.create()
        if user is None:
            user = UserFactory.create()

        return Like.objects.create(
            post=post,
            user=user,
        )


@pytest.fixture
def api_client():
    """Fixture for APIClient."""
    return APIClient()


@pytest.fixture
def user_factory():
    """Fixture for UserFactory."""
    return UserFactory()


@pytest.fixture
def authenticated_client(api_client, user_factory):
    """Fixture for authenticated APIClient."""
    user = user_factory.create(username='authuser')
    token = Token.objects.create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return api_client, user, token


@pytest.fixture
def post_factory():
    """Fixture for PostFactory."""
    return PostFactory()


@pytest.fixture
def comment_factory():
    """Fixture for CommentFactory."""
    return CommentFactory()


@pytest.fixture
def like_factory():
    """Fixture for LikeFactory."""
    return LikeFactory()


@pytest.fixture
def two_users():
    """Fixture for creating two different users."""
    user1 = UserFactory.create(username='user1')
    user2 = UserFactory.create(username='user2')
    return user1, user2


@pytest.fixture
def two_authenticated_clients(api_client, two_users):
    """Fixture for two authenticated clients."""
    user1, user2 = two_users
    token1 = Token.objects.create(user=user1)
    token2 = Token.objects.create(user=user2)

    client1 = APIClient()
    client1.credentials(HTTP_AUTHORIZATION=f'Token {token1.key}')

    client2 = APIClient()
    client2.credentials(HTTP_AUTHORIZATION=f'Token {token2.key}')

    return (client1, user1, token1), (client2, user2, token2)
