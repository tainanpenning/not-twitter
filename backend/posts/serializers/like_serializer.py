from rest_framework import serializers

from posts.models.like import Like


class LikeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    post_id = serializers.IntegerField(source='post.id', read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'username', 'post_id', 'created_at']
        read_only_fields = ['id', 'username', 'post_id', 'created_at']
