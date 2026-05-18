import cloudinary.uploader

from PIL import Image, UnidentifiedImageError

from django.db import transaction
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from accounts.models.profile import Profile
from accounts.models.follow import Follow

ALLOWED_IMAGE_TYPES = [
    'image/jpeg',
    'image/png',
    'image/webp',
    'image/gif',
]

MAX_AVATAR_SIZE = 5 * 1024 * 1024  # 5MB
MAX_IMAGE_DIMENSION = 5000


def validate_avatar(value):
    if not value:
        return value

    content_type = getattr(value, 'content_type', None)

    if content_type not in ALLOWED_IMAGE_TYPES:
        raise serializers.ValidationError('Unsupported file type. Allowed types are: JPEG, PNG, WEBP, GIF.')

    if value.size > MAX_AVATAR_SIZE:
        raise serializers.ValidationError('Avatar image size should not exceed 5MB.')

    try:
        image = Image.open(value)
        image.verify()

        value.seek(0)

        image = Image.open(value)

        if image.width > MAX_IMAGE_DIMENSION or image.height > MAX_IMAGE_DIMENSION:
            raise serializers.ValidationError('Image dimensions are too large.')

    except (UnidentifiedImageError, OSError):
        raise serializers.ValidationError('Invalid image file.')

    finally:
        value.seek(0)

    return value


def upload_avatar(image_file):
    validate_avatar(image_file)

    upload = cloudinary.uploader.upload(
        image_file,
        folder='not-twitter/files',
    )

    return upload['secure_url']


def delete_avatar(public_id):
    if public_id:
        cloudinary.uploader.destroy(public_id)


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    followers_count = serializers.IntegerField(source='_followers_count', read_only=True)
    following_count = serializers.IntegerField(source='_following_count', read_only=True)
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Profile

        fields = [
            'id',
            'user_id',
            'username',
            'display_name',
            'email',
            'bio',
            'birth_date',
            'avatar',
            'followers_count',
            'following_count',
            'is_following',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'user_id',
            'username',
            'email',
            'created_at',
            'updated_at',
        ]

    def get_is_following(self, obj):
        request = self.context.get('request')

        if not request or request.user.is_anonymous:
            return False

        return Follow.objects.filter(
            follower=request.user,
            following=obj.user,
        ).exists()


class ProfileUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', required=False)
    password = serializers.CharField(write_only=True, required=False, min_length=8)
    password_confirm = serializers.CharField(write_only=True, required=False, min_length=8)
    avatar = serializers.ImageField(required=False, write_only=True)

    class Meta:
        model = Profile

        fields = [
            'display_name',
            'bio',
            'birth_date',
            'email',
            'password',
            'password_confirm',
            'avatar',
        ]

    def validate_display_name(self, data):
        if not data:
            return data

        data = data.strip()

        if not data:
            raise serializers.ValidationError('Display name cannot be empty.')

        if len(data) > 30:
            raise serializers.ValidationError('Display name cannot exceed 30 characters.')

        return data

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if password and not password_confirm:
            raise serializers.ValidationError({'password_confirm': 'Confirmation required'})

        if password and password != password_confirm:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match'})

        if password:
            validate_password(password, self.instance.user if self.instance else None)

        return data

    @transaction.atomic
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        password = validated_data.pop('password', None)
        validated_data.pop('password_confirm', None)
        image_file = validated_data.pop('avatar', None)
        email = user_data.get('email')

        if email:
            instance.user.email = email

        if password:
            instance.user.set_password(password)

        instance.user.save()

        if image_file is not None:
            old_avatar = instance.avatar

            new_avatar = upload_avatar(image_file)

            validated_data['avatar'] = new_avatar

            if old_avatar:
                delete_avatar(old_avatar)

        return super().update(instance, validated_data)


class UserSearchSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile

        fields = [
            'id',
            'username',
            'display_name',
            'avatar',
        ]
