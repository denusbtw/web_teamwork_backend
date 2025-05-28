from rest_framework import serializers

from web_teamwork.hackathons.models import Participant
from web_teamwork.users.api.v1.serializers import UserNestedSerializer
from . import HackathonListSerializer


class BaseParticipantReadSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    hackathon = HackathonListSerializer()
    user = UserNestedSerializer()
    status = serializers.CharField(source="get_status_display")


class ParticipantListSerializer(BaseParticipantReadSerializer):
    pass


class ParticipantDetailSerializer(BaseParticipantReadSerializer):
    pass


class ParticipantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ("user",)

    def to_representation(self, instance):
        return ParticipantListSerializer(instance, context=self.context).data


class ParticipantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ("status",)

    def to_representation(self, instance):
        return ParticipantListSerializer(instance, context=self.context).data
