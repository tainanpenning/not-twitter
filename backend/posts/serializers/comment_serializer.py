from rest_framework import serializers

from posts.models.comment import Comment


class CommentSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_display_name = serializers.CharField(source='author.profile.display_name', read_only=True)
    author_avatar = serializers.URLField(source='author.profile.avatar', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'author_id',
            'author_username',
            'author_display_name',
            'author_avatar',
            'post',
            'content',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'author_id',
            'author_username',
            'author_display_name',
            'author_avatar',
            'post',
            'created_at',
        ]
