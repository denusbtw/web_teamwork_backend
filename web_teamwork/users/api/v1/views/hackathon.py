from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions

from web_teamwork.core.api.v1.permissions import ReadOnly
from web_teamwork.hackathons.api.v1.permissions import IsHackathonHost
from web_teamwork.hackathons.api.v1.serializers import (
    ParticipantDetailSerializer,
    ParticipantListSerializer,
)
from web_teamwork.hackathons.models import Participant
from ..filters import UserParticipantFilterSet
from ..permissions import IsSelf


class UserParticipantListAPIView(generics.ListAPIView):
    serializer_class = ParticipantListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserParticipantFilterSet

    def get_queryset(self):
        return Participant.objects.filter(user_id=self.kwargs.get("user_id"))


class UserParticipantRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = ParticipantDetailSerializer
    permission_classes = [ReadOnly | permissions.IsAdminUser | IsHackathonHost | IsSelf]

    def get_queryset(self):
        return Participant.objects.filter(user_id=self.kwargs["user_id"])

    def get_hackathon_id(self):
        participant = Participant.objects.only("hackathon_id").get(pk=self.kwargs["pk"])
        return participant.hackathon_id
