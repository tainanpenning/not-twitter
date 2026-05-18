import pytest
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken


@pytest.mark.django_db
class TestRegisterViewSet:
    """Tests for the registration endpoint."""

    def test_register_user_success(self, api_client):
        """Should register a new user successfully."""
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'ps574839', 'password_confirm': 'ps574839'}
        response = api_client.post('/api/auth/register/', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert 'access' in response.data
        assert response.data['user'] == {'id': 1, 'username': 'newuser'}

    def test_register_password_too_short(self, api_client):
        """Password must have at least 8 characters."""
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'short', 'password_confirm': 'short'}
        response = api_client.post('/api/auth/register/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_password_mismatch(self, api_client):
        """Passwords must match."""
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'ps574839', 'password_confirm': 'wrongpass123'}
        response = api_client.post('/api/auth/register/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_duplicate_email(self, api_client, user_factory):
        """Should not allow duplicate emails."""
        user_factory(email='existing@example.com')

        data = {'username': 'newuser', 'email': 'existing@example.com', 'password': 'ps574839', 'password_confirm': 'ps57483939'}
        response = api_client.post('/api/auth/register/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_duplicate_username(self, api_client, user_factory):
        """Should not allow duplicate usernames."""
        user_factory(username='existing')

        data = {'username': 'existing', 'email': 'newemail@example.com', 'password': 'ps574839', 'password_confirm': 'ps57483939'}
        response = api_client.post('/api/auth/register/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLoginViewSet:
    """Tests for the login endpoint."""

    def test_login_success(self, api_client, user_factory):
        """Should log in with correct credentials."""
        user_factory(username='testuser', password='ps574839')

        data = {'identifier': 'testuser', 'password': 'ps574839'}
        response = api_client.post('/api/auth/login/', data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data

    def test_login_invalid_username(self, api_client):
        """Should fail with invalid username."""
        data = {'identifier': 'nonexistent', 'password': 'ps574839'}
        response = api_client.post('/api/auth/login/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_invalid_password(self, api_client, user_factory):
        """Should fail with invalid password."""
        user_factory(username='testuser', password='ps574839')

        data = {'identifier': 'testuser', 'password': 'wrongpass'}
        response = api_client.post('/api/auth/login/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLogoutViewSet:
    """Tests for the logout endpoint."""

    def test_logout_success(self, authenticated_client):
        client, user, refresh = authenticated_client

        jti = refresh['jti']

        response = client.post('/api/auth/logout/', {'refresh': str(refresh)}, format='json')

        assert response.status_code == status.HTTP_200_OK

        assert BlacklistedToken.objects.filter(token__jti=jti).exists()

    def test_logout_unauthorized(self, api_client):
        response = api_client.post('/api/auth/logout/', {}, format='json')

        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED]


@pytest.mark.django_db
class TestProfileViewSet:
    """Tests for the profile endpoint."""

    def test_get_profile(self, authenticated_client):
        """Should return the profile of the user."""
        client, user, token = authenticated_client

        response = client.get(f'/api/profiles/{user.username}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == user.username
        assert response.data['display_name'] == user.profile.display_name

    def test_get_profile_me(self, authenticated_client):
        """Should return the profile of the current user with 'me'."""
        client, user, token = authenticated_client

        response = client.get('/api/profiles/me/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == user.username

    def test_update_own_profile(self, authenticated_client):
        """Should allow updating the own profile."""
        client, user, token = authenticated_client

        data = {'display_name': 'New Name', 'bio': 'New bio'}
        response = client.put(f'/api/profiles/me/', data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['display_name'] == 'New Name'

    def test_search_users(self, authenticated_client, profile_factory):
        """Should search users by username."""
        client, user, token = authenticated_client
        profile_factory(username='john_doe', display_name='John')

        response = client.get('/api/profiles/?q=john')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0
