import pytest

from web_teamwork.hackathons.api.v1.serializers import (
    HackathonUpdateSerializer,
)
from web_teamwork.hackathons.api.v1.serializers.hackathon import (
    BaseHackathonReadSerializer,
)


@pytest.mark.django_db
class TestBaseHackathonReadSerializer:

    def test_prize_is_formatted_correctly(self, hackathon_factory):
        hackathon = hackathon_factory(prize=1000)
        serializer = BaseHackathonReadSerializer(hackathon)
        assert serializer.data["prize"] == "1000$"


@pytest.mark.django_db
class TestHackathonUpdateSerializer:

    def test_no_error_if_empty_data(self, hackathon_factory):
        hackathon = hackathon_factory()
        serializer = HackathonUpdateSerializer(hackathon, data={})
        assert serializer.is_valid(), serializer.errors
