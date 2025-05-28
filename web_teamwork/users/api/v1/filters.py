from django_filters import rest_framework as filters

from web_teamwork.hackathons.models import Participant


class UserParticipantFilterSet(filters.FilterSet):
    status = filters.ChoiceFilter(choices=Participant.Status.choices)

    class Meta:
        model = Participant
        fields = ("status",)
