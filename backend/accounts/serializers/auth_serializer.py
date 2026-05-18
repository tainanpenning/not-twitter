import re

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')

    def validate_username(self, data):
        data = data.strip()

        if len(data) < 3:
            raise serializers.ValidationError("Username too short.")

        if len(data) > 30:
            raise serializers.ValidationError("Username too lange.")

        if not re.match(r'^[a-zA-Z0-9_]+$', data):
            raise serializers.ValidationError("Use just letters, numbers and '_'")

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

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        user = User.objects.create_user(username=validated_data['username'], email=validated_data['email'], password=validated_data['password'])
        return user


class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        identifier = data.get("identifier")
        password = data.get("password")

        if "@" in identifier:
            user = User.objects.filter(email=identifier).first()

        else:
            user = User.objects.filter(username=identifier).first()

        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        authenticated = authenticate(
            username=user.username,
            password=password,
        )

        if not authenticated:
            raise serializers.ValidationError("Invalid credentials.")

        if not authenticated.is_active:
            raise serializers.ValidationError("User inactive.")

        data["user"] = authenticated

        return data
