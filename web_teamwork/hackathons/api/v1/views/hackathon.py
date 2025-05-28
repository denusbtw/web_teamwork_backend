from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters

from web_teamwork.core.api.v1.permissions import ReadOnly
from web_teamwork.hackathons.models import Hackathon
from web_teamwork.users.api.v1.permissions import IsHost
from ..filters import HackathonFilterSet
from ..permissions import IsHackathonHost
from ..serializers import (
    HackathonListSerializer,
    HackathonCreateSerializer,
    HackathonDetailSerializer,
    HackathonUpdateSerializer,
)


class HackathonListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [ReadOnly | permissions.IsAdminUser | IsHost]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = ("title",)
    ordering_fields = ("prize", "start_datetime")
    ordering = "-created_at"
    filterset_class = HackathonFilterSet

    def get_queryset(self):
        return Hackathon.objects.filter(end_datetime__gte=timezone.now())

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return HackathonListSerializer
        return HackathonCreateSerializer

    def perform_create(self, serializer):
        serializer.save(hosted_by=self.request.user)


class HackathonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hackathon.objects.all()
    permission_classes = [ReadOnly | permissions.IsAdminUser | IsHackathonHost]

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return HackathonDetailSerializer
        return HackathonUpdateSerializer

    def get_hackathon_id(self):
        return self.kwargs.get("pk")
