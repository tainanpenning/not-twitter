from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=300)
    media = models.FileField(upload_to='post_media/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by @{self.author.username} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    @property
    def likes_count(self):
        if hasattr(self, '_likes_count'):
            return self._likes_count
        return self.likes.count()

    @property
    def comments_count(self):
        if hasattr(self, '_comments_count'):
            return self._comments_count
        return self.comments.count()
