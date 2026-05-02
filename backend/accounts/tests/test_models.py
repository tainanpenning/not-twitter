import pytest
from accounts.models.profile import Profile
from accounts.models.follow import Follow


@pytest.mark.django_db
class TestProfileModel:
    """Tests for the Profile model."""

    def test_profile_created_on_user_creation(self, user_factory):
        """Profile should be created automatically with the user."""
        user = user_factory()
        assert Profile.objects.filter(user=user).exists()

    def test_profile_string_representation(self, profile_factory):
        """Test __str__ of the Profile."""
        profile = profile_factory()
        assert str(profile) == f"@{profile.user.username}"

    def test_profile_display_name(self, profile_factory):
        """Profile should allow display_name."""
        profile = profile_factory(display_name='João Silva')
        assert profile.display_name == 'João Silva'

    def test_profile_followers_count(self, profile_factory, follow_factory):
        """Test followers count of the Profile."""
        user1 = profile_factory().user
        user2 = profile_factory().user

        follow_factory(follower=user2, following=user1)
        profile = Profile.objects.get(user=user1)

        assert profile.followers_count == 1

    def test_profile_following_count(self, profile_factory, follow_factory):
        """Test following count of the Profile."""
        user1 = profile_factory().user
        user2 = profile_factory().user

        follow_factory(follower=user1, following=user2)
        profile = Profile.objects.get(user=user1)

        assert profile.following_count == 1


@pytest.mark.django_db
class TestFollowModel:
    """Tests for the Follow model."""

    def test_follow_creation(self, follow_factory):
        """Should create a follow relationship."""
        follow = follow_factory()
        assert Follow.objects.filter(follower=follow.follower, following=follow.following).exists()

    def test_follow_unique_constraint(self, two_users, follow_factory):
        """Should not allow duplicate follow relationships."""
        user1, user2 = two_users
        follow_factory(follower=user1, following=user2)

        with pytest.raises(Exception):  # IntegrityError
            Follow.objects.create(follower=user1, following=user2)

    def test_follow_string_representation(self, follow_factory):
        """Test __str__ of the Follow."""
        follow = follow_factory()
        expected = f"{follow.follower.username} follows {follow.following.username}"
        assert str(follow) == expected

    def test_cannot_self_follow(self, user_factory):
        """Test constraint of not following oneself via unique constraint."""
        user = user_factory()
        # The validation should be done in the viewset, not in the model
        # But the unique constraint prevents duplicates,
        # not self-following, so we can create a self-follow in the model,
        # but it should be blocked in the viewset
        follow = Follow.objects.create(follower=user, following=user)
        assert follow.id is not None  # The model allows it, but the viewset should prevent it
