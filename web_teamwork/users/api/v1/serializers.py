from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserNestedSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    username = serializers.CharField()
    email = serializers.EmailField()
    full_name = serializers.CharField(source="get_full_name")


class BaseUserReadSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()
    username = serializers.CharField()
    full_name = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url
        return settings.STATIC_URL + "images/default/profile_picture.png"

    def get_role(self, obj):
        return obj.get_role_display()


class UserListSerializer(BaseUserReadSerializer):
    pass


class UserDetailSerializer(BaseUserReadSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    date_joined = serializers.DateTimeField()
    profile_background = serializers.SerializerMethodField()

    def get_profile_background(self, obj):
        if obj.profile_background:
            return obj.profile_background.url
        return settings.STATIC_URL + "images/default/profile_background.jpg"


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "role", "email", "password")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "profile_picture",
            "profile_background",
        )
        extra_kwargs = {
            "email": {"required": False},
        }
