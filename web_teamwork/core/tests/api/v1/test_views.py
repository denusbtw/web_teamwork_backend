import pytest
from django.urls import reverse
from django.utils import timezone


@pytest.fixture
def url():
    return reverse("api:v1:leaderboard")


@pytest.mark.django_db
class TestLeaderboardAPIView:

    def test_das(self, api_client, url, hackathon_factory, user_factory):
        user1 = user_factory()
        user2 = user_factory()
        user3 = user_factory()
        user4 = user_factory()

        hackathon_factory(prize=1000, winner=user1, end_datetime=timezone.now())
        hackathon_factory(prize=200, winner=user2, end_datetime=timezone.now())
        hackathon_factory(prize=300, winner=user1, end_datetime=timezone.now())
        hackathon_factory(prize=900, winner=user3, end_datetime=timezone.now())

        response = api_client.get(url)
        print(response.data)
