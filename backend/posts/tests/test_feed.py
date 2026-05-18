import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models.follow import Follow
from posts.tests.conftest import UserFactory, PostFactory


@pytest.mark.django_db
class TestFeedViewSet:
    """Test suite for Feed viewset."""

    def test_feed_shows_followed_authors_posts(self):
        """Test feed shows posts from followed authors."""
        user = UserFactory.create()
        author1 = UserFactory.create()
        author2 = UserFactory.create()

        # Create follow relationship
        Follow.objects.create(follower=user, following=author1)

        # Create posts
        post1 = PostFactory.create(author=author1, content='Post from author1')
        post2 = PostFactory.create(author=author2, content='Post from author2')

        # Authenticate as user
        token = RefreshToken.for_user(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token.access_token)}')

        # Get feed
        response = client.get('/api/posts/feed/')
        assert response.status_code == status.HTTP_200_OK

        # Should only see post1 (from followed author)
        post_ids = [p['id'] for p in response.data['results']]
        assert post1.id in post_ids
        assert post2.id not in post_ids

    def test_feed_excludes_own_posts(self):
        """Test feed includes user's own posts."""
        user = UserFactory.create()

        # Create post by user
        post = PostFactory.create(author=user)

        token = RefreshToken.for_user(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token.access_token)}')

        response = client.get('/api/posts/feed/')
        assert response.status_code == status.HTTP_200_OK
        # Own posts should not appear in feed (follow relationships required)
        post_ids = [p['id'] for p in response.data['results']]
        assert post.id not in post_ids

    def test_feed_unauthenticated(self):
        """Test feed requires authentication."""
        client = APIClient()
        response = client.get('/api/posts/feed/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_feed_pagination(self):
        """Test feed pagination."""
        user = UserFactory.create()
        author = UserFactory.create()
        Follow.objects.create(follower=user, following=author)

        # Create 25 posts
        for i in range(25):
            PostFactory.create(author=author)

        token = RefreshToken.for_user(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token.access_token)}')

        response = client.get('/api/posts/feed/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 20  # First page with 20 items
        assert response.data['next'] is not None  # Should have next page
