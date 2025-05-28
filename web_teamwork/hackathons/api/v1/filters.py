from django_filters import rest_framework as filters

from web_teamwork.hackathons.models import Hackathon


class HackathonFilterSet(filters.FilterSet):
    category = filters.CharFilter(field_name="category__slug", lookup_expr="iexact")
    hosted_by = filters.CharFilter(
        field_name="hosted_by__username", lookup_expr="iexact"
    )
    start_after = filters.DateTimeFilter(field_name="start_datetime", lookup_expr="gte")
    end_before = filters.DateTimeFilter(field_name="end_datetime", lookup_expr="lte")

    class Meta:
        model = Hackathon
        fields = ("category", "hosted_by", "start_after", "end_before", "title")
