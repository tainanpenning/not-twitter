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
        raise serializers.ValidationError(('Unsupported file type. ' 'Allowed: JPEG, PNG, WEBP, GIF, MP4.'))

    max_size = 25 * 1024 * 1024

    if value.size > max_size:
        raise serializers.ValidationError(('Media file size ' 'should not exceed 25MB.'))

    return value


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_display_name = serializers.SerializerMethodField()
    author_avatar = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

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

        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]

    def get_author_display_name(self, obj):
        profile = getattr(obj.author, 'profile', None)

        if not profile:
            return None

        return profile.display_name

    def get_author_avatar(self, obj):
        profile = getattr(obj.author, 'profile', None)

        if not profile:
            return None

        return profile.avatar

    def get_likes_count(self, obj):
        return getattr(obj, '_likes_count', 0)

    def get_comments_count(self, obj):
        return getattr(obj, '_comments_count', 0)

    def get_is_liked(self, obj):
        return getattr(obj, '_is_liked', False)


class PostWriteSerializer(serializers.ModelSerializer):
    media = serializers.FileField(
        required=False,
        allow_null=True,
        validators=[validate_media],
    )

    class Meta:
        model = Post

        fields = ['content', 'media']

    def _upload_media(self, validated_data):
        media_file = validated_data.pop('media', None)

        if not media_file:
            return validated_data

        upload = cloudinary.uploader.upload(
            media_file,
            folder='not-twitter/files',
        )

        validated_data['media'] = upload['secure_url']

        return validated_data

    def create(self, validated_data):
        validated_data = self._upload_media(validated_data)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data = self._upload_media(validated_data)

        return super().update(instance, validated_data)
