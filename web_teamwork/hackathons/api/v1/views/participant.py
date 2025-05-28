from rest_framework import generics, permissions

from web_teamwork.core.api.v1.permissions import ReadOnly
from web_teamwork.hackathons.models import Participant
from ..permissions import (
    IsHackathonHost,
    ParticipantCanDeleteSelf,
)
from ..serializers import (
    ParticipantListSerializer,
    ParticipantCreateSerializer,
    ParticipantDetailSerializer,
    ParticipantUpdateSerializer,
)


class HackathonParticipantListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [
        ReadOnly | permissions.IsAdminUser | permissions.IsAuthenticated
    ]

    def get_queryset(self):
        return Participant.objects.filter(hackathon_id=self.kwargs.get("hackathon_id"))

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return ParticipantListSerializer
        return ParticipantCreateSerializer

    def perform_create(self, serializer):
        serializer.save(hackathon_id=self.kwargs.get("hackathon_id"))


class HackathonParticipantRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    permission_classes = [
        ReadOnly | permissions.IsAdminUser | IsHackathonHost | ParticipantCanDeleteSelf
    ]

    def get_queryset(self):
        return Participant.objects.filter(hackathon_id=self.kwargs.get("hackathon_id"))

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return ParticipantDetailSerializer
        return ParticipantUpdateSerializer
