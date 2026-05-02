import pytest
from rest_framework import status


@pytest.mark.django_db
class TestFollowViewSet:
    """Tests for the following/unfollowing functionality."""

    def test_follow_user(self, authenticated_client, user_factory):
        """Should follow a user successfully."""
        client, user, token = authenticated_client
        target_user = user_factory(username='target')

        response = client.post(f'/api/accounts/follow/toggle/{target_user.username}/', format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['detail'] == 'Followed successfully.'

    def test_unfollow_user(self, authenticated_client, user_factory, follow_factory):
        """Should unfollow a user successfully."""
        client, user, token = authenticated_client
        target_user = user_factory(username='target')
        follow_factory(follower=user, following=target_user)

        response = client.post(f'/api/accounts/follow/toggle/{target_user.username}/', format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['detail'] == 'Unfollowed successfully.'

    def test_cannot_follow_self(self, authenticated_client):
        """Should not allow following oneself."""
        client, user, token = authenticated_client

        response = client.post(f'/api/accounts/follow/toggle/{user.username}/', format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'cannot follow yourself' in response.data['detail'].lower()

    def test_followers_list(self, authenticated_client, user_factory, follow_factory):
        """Should list followers of the user."""
        client, user, token = authenticated_client
        follower = user_factory(username='follower')
        follow_factory(follower=follower, following=user)

        response = client.get(f'/api/accounts/follow/followers/{user.username}/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0

    def test_following_list(self, authenticated_client, user_factory, follow_factory):
        """Should list users that the user is following."""
        client, user, token = authenticated_client
        following = user_factory(username='following')
        follow_factory(follower=user, following=following)

        response = client.get(f'/api/accounts/follow/following/{user.username}/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0

    def test_follow_unauthorized(self, api_client, user_factory):
        """Should reject follow without authentication."""
        target_user = user_factory(username='target')

        response = api_client.post(f'/api/accounts/follow/toggle/{target_user.username}/', format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
