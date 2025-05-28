import pytest
from django.urls import reverse
from rest_framework import status


@pytest.fixture
def list_url(user):
    return reverse("api:v1:user_hackathon_list", kwargs={"user_id": user.pk})


@pytest.fixture
def detail_url(participant):
    return reverse(
        "api:v1:user_participant_detail",
        kwargs={"user_id": participant.user_id, "pk": participant.pk},
    )


@pytest.mark.django_db
class TestUserHackathonListAPIView:

    def test_lists_hackathons_only_of_requested_user(
        self, api_client, list_url, user, participant_factory
    ):
        participant_factory.create_batch(2, user=user)
        participant_factory.create_batch(3)

        response = api_client.get(list_url)
        assert response.status_code == status.HTTP_200_OK

    class TestPermissions:

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [("get", status.HTTP_200_OK), ("post", status.HTTP_405_METHOD_NOT_ALLOWED)],
        )
        def test_anonymous_user(
            self, api_client, list_url, method, expected_status_code
        ):
            response = getattr(api_client, method)(list_url)
            assert response.status_code == expected_status_code


@pytest.mark.django_db
class TestUserParticipantRetrieveDestroyAPIView:

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
            self, api_client, detail_url, user_factory, method, expected_status_code
        ):
            user = user_factory()
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
        def test_self_user(
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
        def test_admin_user(
            self, api_client, detail_url, admin_user, method, expected_status_code
        ):
            api_client.force_authenticate(user=admin_user)
            response = getattr(api_client, method)(detail_url)
            assert response.status_code == expected_status_code
