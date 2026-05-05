import pytest
from rest_framework import status
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
class TestRegisterViewSet:
    """Tests for the registration endpoint."""

    def test_register_user_success(self, api_client):
        """Should register a new user successfully."""
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'testpass123', 'password_confirm': 'testpass123'}
        response = api_client.post('/api/accounts/auth/register/', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert 'token' in response.data
        assert response.data['username'] == 'newuser'

    def test_register_password_too_short(self, api_client):
        """Password must have at least 8 characters."""
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'short', 'password_confirm': 'short'}
        response = api_client.post('/api/accounts/auth/register/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_password_mismatch(self, api_client):
        """Passwords must match."""
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'testpass123', 'password_confirm': 'wrongpass123'}
        response = api_client.post('/api/accounts/auth/register/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_duplicate_email(self, api_client, user_factory):
        """Should not allow duplicate emails."""
        user_factory(email='existing@example.com')

        data = {'username': 'newuser', 'email': 'existing@example.com', 'password': 'testpass123', 'password_confirm': 'testpass123'}
        response = api_client.post('/api/accounts/auth/register/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_duplicate_username(self, api_client, user_factory):
        """Should not allow duplicate usernames."""
        user_factory(username='existing')

        data = {'username': 'existing', 'email': 'newemail@example.com', 'password': 'testpass123', 'password_confirm': 'testpass123'}
        response = api_client.post('/api/accounts/auth/register/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLoginViewSet:
    """Tests for the login endpoint."""

    def test_login_success(self, api_client, user_factory):
        """Should log in with correct credentials."""
        user_factory(username='testuser', password='testpass123')

        data = {'username': 'testuser', 'password': 'testpass123'}
        response = api_client.post('/api/accounts/auth/login/', data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data

    def test_login_invalid_username(self, api_client):
        """Should fail with invalid username."""
        data = {'username': 'nonexistent', 'password': 'testpass123'}
        response = api_client.post('/api/accounts/auth/login/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_invalid_password(self, api_client, user_factory):
        """Should fail with invalid password."""
        user_factory(username='testuser', password='testpass123')

        data = {'username': 'testuser', 'password': 'wrongpass'}
        response = api_client.post('/api/accounts/auth/login/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLogoutViewSet:
    """Tests for the logout endpoint."""

    def test_logout_success(self, authenticated_client):
        """Should log out successfully."""
        client, user, token = authenticated_client

        response = client.post('/api/accounts/auth/logout/')

        assert response.status_code == status.HTTP_200_OK
        # Token should be deleted
        assert not Token.objects.filter(user=token.user).exists()

    def test_logout_unauthorized(self, api_client):
        """Should reject logout without authentication."""
        response = api_client.post('/api/accounts/auth/logout/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestProfileViewSet:
    """Tests for the profile endpoint."""

    def test_get_profile(self, authenticated_client):
        """Should return the profile of the user."""
        client, user, token = authenticated_client

        response = client.get(f'/api/accounts/profiles/{user.username}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == user.username
        assert response.data['display_name'] == user.profile.display_name

    def test_get_profile_me(self, authenticated_client):
        """Should return the profile of the current user with 'me'."""
        client, user, token = authenticated_client

        response = client.get('/api/accounts/profiles/me/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == user.username

    def test_update_own_profile(self, authenticated_client):
        """Should allow updating the own profile."""
        client, user, token = authenticated_client

        data = {'display_name': 'New Name', 'bio': 'New bio'}
        response = client.put(f'/api/accounts/profiles/{user.username}/', data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['display_name'] == 'New Name'

    def test_cannot_update_others_profile(self, authenticated_client, profile_factory):
        """Should not allow updating the profile of another user."""
        client, user, token = authenticated_client
        other_profile = profile_factory(username='otheruser')

        data = {'display_name': 'Hacked Name'}
        response = client.put(f'/api/accounts/profiles/{other_profile.user.username}/', data, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_search_users(self, authenticated_client, profile_factory):
        """Should search users by username."""
        client, user, token = authenticated_client
        profile_factory(username='john_doe', display_name='John')

        response = client.get('/api/accounts/search/?q=john')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0
