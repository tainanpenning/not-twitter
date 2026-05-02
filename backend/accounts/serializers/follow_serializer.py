from rest_framework import serializers

from accounts.models.follow import Follow


class FollowSerializer(serializers.ModelSerializer):
    follower_username = serializers.CharField(source='follower.username', read_only=True)
    following_username = serializers.CharField(source='following.username', read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower_username', 'following_username', 'created_at']
        read_only_fields = ['id', 'follower_username', 'following_username', 'created_at']

    def validate(self, data):
        follower = self.context['request'].user
        following = data.get('following')

        if follower == following:
            raise serializers.ValidationError("You cannot follow yourself.")
        if Follow.objects.filter(follower=follower, following=following).exists():
            raise serializers.ValidationError("You are already following this user.")
        return data
