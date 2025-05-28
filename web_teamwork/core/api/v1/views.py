from django.contrib.auth import get_user_model
from django.db.models import Sum, Value, Q
from django.db.models.functions import Coalesce
from django.utils import timezone
from rest_framework import generics, filters
from rest_framework.exceptions import ValidationError

from .serializers import UserLeaderboardSerializer

User = get_user_model()


class LeaderboardAPIView(generics.ListAPIView):
    serializer_class = UserLeaderboardSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("email",)

    def get_queryset(self):
        period = self.request.query_params.get("period", "today")
        if period not in {"today", "month", "year"}:
            raise ValidationError("Invalid period")

        time_filter = self.get_time_filter(period)

        return User.objects.annotate(
            total_prize=Coalesce(
                Sum(
                    "won_hackathons__prize",
                    filter=Q(won_hackathons__end_datetime__gte=time_filter),
                ),
                Value(0),
            )
        ).order_by("-total_prize")

    def get_time_filter(self, period):
        now = timezone.now()

        match period:
            case "today":
                return now.replace(hour=0, minute=0, second=0, microsecond=0)
            case "month":
                return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            case "year":
                return now.replace(
                    month=1, day=1, hour=0, minute=0, second=0, microsecond=0
                )
            case _:
                return None
