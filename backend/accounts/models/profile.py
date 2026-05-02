from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"@{self.user.username}"

    @property
    def followers_count(self):
        if hasattr(self, '_followers_count'):
            return self._followers_count
        return self.user.followers.count()

    @property
    def following_count(self):
        if hasattr(self, '_following_count'):
            return self._following_count
        return self.user.following.count()
