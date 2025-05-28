import pytest

from web_teamwork.hackathons.api.v1.serializers import (
    ParticipantUpdateSerializer,
)
from web_teamwork.hackathons.api.v1.serializers.participant import (
    BaseParticipantReadSerializer,
)


@pytest.mark.django_db
class TestBaseParticipantReadSerializer:

    def test_status_is_human_friendly(self, participant_factory):
        participant = participant_factory()
        serializer = BaseParticipantReadSerializer(participant)
        assert serializer.data["status"] == participant.get_status_display()


@pytest.mark.django_db
class TestParticipantUpdateSerializer:

    def test_no_error_if_empty_data(self, participant_factory):
        participant = participant_factory()
        serializer = ParticipantUpdateSerializer(participant, data={})
        assert serializer.is_valid(), serializer.errors
