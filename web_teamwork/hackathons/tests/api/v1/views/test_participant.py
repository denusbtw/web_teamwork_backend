import pytest
from django.urls import reverse
from rest_framework import status

from web_teamwork.conftest import hackathon, participant
from web_teamwork.hackathons.models import Participant


@pytest.fixture
def list_url(hackathon):
    return reverse("api:v1:participant_list", kwargs={"hackathon_id": hackathon.pk})


@pytest.fixture
def detail_url(participant):
    return reverse(
        "api:v1:participant_detail",
        kwargs={"hackathon_id": participant.hackathon_id, "pk": participant.pk},
    )


@pytest.fixture
def data(user_factory):
    user = user_factory()
    return {"user": user.pk}


@pytest.mark.django_db
class TestHackathonParticipantListCreateAPIView:

    def test_lists_only_requested_hackathon_participants(
        self,
        api_client,
        list_url,
        hackathon,
        hackathon_factory,
        participant_factory,
    ):
        another_hackathon = hackathon_factory()
        participant_factory.create_batch(2, hackathon=hackathon)
        participant_factory.create_batch(3, hackathon=another_hackathon)

        response = api_client.get(list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    class TestPermissions:

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("post", status.HTTP_403_FORBIDDEN),
            ],
        )
        def test_anonymous_user(
            self, api_client, list_url, method, expected_status_code
        ):
            response = getattr(api_client, method)(list_url)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("post", status.HTTP_403_FORBIDDEN),
            ],
        )
        def test_authenticated_user(
            self, api_client, user, list_url, method, expected_status_code
        ):
            api_client.force_authenticate(user=user)
            response = getattr(api_client, method)(list_url)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("post", status.HTTP_403_FORBIDDEN),
            ],
        )
        def test_host_but_not_hackathon_host_user(
            self, api_client, host_user, list_url, method, expected_status_code
        ):
            api_client.force_authenticate(user=host_user)
            response = getattr(api_client, method)(list_url)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("post", status.HTTP_201_CREATED),
            ],
        )
        def test_hackathon_host(
            self, api_client, hackathon, list_url, data, method, expected_status_code
        ):
            api_client.force_authenticate(user=hackathon.hosted_by)
            response = getattr(api_client, method)(list_url, data=data)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("post", status.HTTP_201_CREATED),
            ],
        )
        def test_admin_user(
            self, api_client, admin_user, list_url, data, method, expected_status_code
        ):
            api_client.force_authenticate(user=admin_user)
            response = getattr(api_client, method)(list_url, data=data)
            assert response.status_code == expected_status_code

    def test_perform_create(self, api_client, list_url, admin_user, hackathon, data):
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(list_url, data=data)
        assert response.status_code == status.HTTP_201_CREATED

        participant_id = response.data["id"]
        participant = Participant.objects.get(pk=participant_id)
        assert participant.hackathon == hackathon


@pytest.mark.django_db
class TestHackathonParticipantRetrieveUpdateDestroyAPIView:

    class TestPermissions:

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("put", status.HTTP_403_FORBIDDEN),
                ("patch", status.HTTP_403_FORBIDDEN),
                ("delete", status.HTTP_403_FORBIDDEN),
            ],
        )
        def test_anonymous_user(
            self, api_client, detail_url, method, expected_status_code
        ):
            response = getattr(api_client, method)(detail_url)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("put", status.HTTP_403_FORBIDDEN),
                ("patch", status.HTTP_403_FORBIDDEN),
                ("delete", status.HTTP_403_FORBIDDEN),
            ],
        )
        def test_authenticated_user(
            self, api_client, detail_url, user, method, expected_status_code
        ):
            api_client.force_authenticate(user=user)
            response = getattr(api_client, method)(detail_url)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("put", status.HTTP_403_FORBIDDEN),
                ("patch", status.HTTP_403_FORBIDDEN),
                ("delete", status.HTTP_403_FORBIDDEN),
            ],
        )
        def test_authenticated_user(
            self, api_client, detail_url, user, method, expected_status_code
        ):
            api_client.force_authenticate(user=user)
            response = getattr(api_client, method)(detail_url)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("put", status.HTTP_403_FORBIDDEN),
                ("patch", status.HTTP_403_FORBIDDEN),
                ("delete", status.HTTP_403_FORBIDDEN),
            ],
        )
        def test_host_user(
            self, api_client, detail_url, host_user, method, expected_status_code
        ):
            api_client.force_authenticate(user=host_user)
            response = getattr(api_client, method)(detail_url)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("put", status.HTTP_200_OK),
                ("patch", status.HTTP_200_OK),
                ("delete", status.HTTP_204_NO_CONTENT),
            ],
        )
        def test_hackathon_host(
            self, api_client, detail_url, hackathon, method, expected_status_code
        ):
            api_client.force_authenticate(user=hackathon.hosted_by)
            response = getattr(api_client, method)(detail_url)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("put", status.HTTP_403_FORBIDDEN),
                ("patch", status.HTTP_403_FORBIDDEN),
                ("delete", status.HTTP_204_NO_CONTENT),
            ],
        )
        def test_self(
            self, api_client, detail_url, participant, method, expected_status_code
        ):
            api_client.force_authenticate(user=participant.user)
            response = getattr(api_client, method)(detail_url)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("put", status.HTTP_200_OK),
                ("patch", status.HTTP_200_OK),
                ("delete", status.HTTP_204_NO_CONTENT),
            ],
        )
        def test_admin(
            self, api_client, detail_url, admin_user, method, expected_status_code
        ):
            api_client.force_authenticate(user=admin_user)
            response = getattr(api_client, method)(detail_url)
            assert response.status_code == expected_status_code
