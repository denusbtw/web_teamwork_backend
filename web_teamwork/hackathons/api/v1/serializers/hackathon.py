from rest_framework import serializers

from web_teamwork.hackathons.models import Hackathon
from web_teamwork.users.api.v1.serializers import UserNestedSerializer
from .category import BaseCategoryReadSerializer


class BaseHackathonReadSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    description = serializers.CharField()
    category = BaseCategoryReadSerializer()
    prize = serializers.SerializerMethodField()
    image = serializers.ImageField()
    start_datetime = serializers.DateTimeField()
    end_datetime = serializers.DateTimeField()

    def get_prize(self, obj):
        return f"{obj.prize}$"


class HackathonListSerializer(BaseHackathonReadSerializer):
    pass


class HackathonDetailSerializer(BaseHackathonReadSerializer):
    winner = UserNestedSerializer()


class HackathonNestedSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()


class HackathonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = (
            "title",
            "description",
            "category",
            "prize",
            "image",
            "start_datetime",
            "end_datetime",
        )

    def to_representation(self, instance):
        return HackathonListSerializer(instance, context=self.context).data


class HackathonUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = (
            "title",
            "description",
            "category",
            "prize",
            "image",
            "start_datetime",
            "end_datetime",
            "winner",
        )
        extra_kwargs = {
            "title": {"required": False},
            "description": {"required": False},
            "prize": {"required": False},
            "image": {"required": False},
            "start_datetime": {"required": False},
            "end_datetime": {"required": False},
        }

    def to_representation(self, instance):
        return HackathonListSerializer(instance, context=self.context).data
