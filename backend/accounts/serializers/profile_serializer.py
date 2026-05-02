from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from PIL import Image, UnidentifiedImageError

from accounts.models.profile import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    followers_count = serializers.IntegerField(read_only=True, default=0)
    following_count = serializers.IntegerField(read_only=True, default=0)
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'user_id', 'username', 'display_name', 'bio', 'birth_date', 'avatar', 'followers_count', 'following_count', 'is_following', 'created_at', 'updated_at']
        read_only_fields = ['id', 'username', 'user_id', 'created_at', 'updated_at']

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.user.followers.filter(follower=request.user).exists()
        return False


class ProfileUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Profile
        fields = ['display_name', 'bio', 'birth_date', 'password', 'avatar']

    def validate_display_name(self, value):
        if value and len(value) > 100:
            raise serializers.ValidationError("Display name cannot exceed 100 characters.")
        return value

    def validate_avatar(self, value):
        if not value:
            return value

        allowed_types = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
        content_type = getattr(value, 'content_type', None)

        if content_type not in allowed_types:
            raise serializers.ValidationError("Unsupported file type. Allowed types are: JPEG, PNG, WEBP, GIF.")

        if value.size > 5 * 1024 * 1024:  # 5MB limit
            raise serializers.ValidationError("Avatar image size should not exceed 5MB.")

        try:
            image = Image.open(value)
            image.verify()  # Verify that it's an actual image
        except (UnidentifiedImageError, OSError):
            raise serializers.ValidationError("Invalid image file.")
        finally:
            value.seek(0)  # Reset file pointer after validation

        return value

    def validate_password(self, value):
        if value:
            validate_password(value, self.instance.user if self.instance else None)
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        if password:
            instance.user.set_password(password)
            instance.user.save()
        return super().update(instance, validated_data)


class UserSearchSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    followers_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user_id', 'username', 'avatar', 'followers_count']
        read_only_fields = ['id', 'user_id', 'username', 'followers_count']
