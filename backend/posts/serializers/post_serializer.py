import cloudinary.uploader
from rest_framework import serializers

from posts.models.post import Post


def validate_media(value):
    if not value:
        return value

    allowed_types = [
        'image/jpeg',
        'image/png',
        'image/webp',
        'image/gif',
        'video/mp4',
    ]
    content_type = getattr(value, 'content_type', None)

    if content_type not in allowed_types:
        raise serializers.ValidationError(
            "Unsupported file type. Allowed types are: JPEG, PNG, WEBP, GIF for images and MP4 for videos.",
        )

    if value.size > 25 * 1024 * 1024:  # 25MB limit
        raise serializers.ValidationError(
            "Media file size should not exceed 25MB.",
        )

    return value


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_display_name = serializers.CharField(source='author.profile.display_name', read_only=True)
    author_avatar = serializers.ImageField(source='author.profile.avatar', read_only=True, allow_null=True)
    likes_count = serializers.IntegerField(source='_likes_count', read_only=True, default=0)
    comments_count = serializers.IntegerField(source='_comments_count', read_only=True, default=0)
    is_liked = serializers.BooleanField(source='_is_liked', read_only=True, default=False)

    class Meta:
        model = Post
        fields = [
            'id',
            'author_username',
            'author_display_name',
            'author_avatar',
            'content',
            'media',
            'likes_count',
            'comments_count',
            'is_liked',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        media_file = validated_data.pop('media', None)

        if media_file:
            validate_media(media_file)

            upload = cloudinary.uploader.upload(media_file, folder='not-twitter/files')

            validated_data['media'] = upload['secure_url']

        return super().create(validated_data)


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content', 'media']

    def update(self, instance, validated_data):
        media_file = validated_data.pop('media', None)

        if media_file:
            validate_media(media_file)

            upload = cloudinary.uploader.upload(media_file, folder='not-twitter/files')

            validated_data['media'] = upload['secure_url']

        return super().update(instance, validated_data)
