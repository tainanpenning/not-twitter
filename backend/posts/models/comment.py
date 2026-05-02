from django.db import models
from django.contrib.auth.models import User

from posts.models.post import Post


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=300)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['author']),
        ]

    def __str__(self):
        return f"Comment by @{self.author.username} on Post ID {self.post.id} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
