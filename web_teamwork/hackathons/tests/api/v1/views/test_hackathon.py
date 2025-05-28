import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from web_teamwork.conftest import hackathon
from web_teamwork.hackathons.models import Hackathon

User = get_user_model()


@pytest.fixture
def list_url():
    return reverse("api:v1:hackathon_list")


@pytest.fixture
def detail_url(hackathon):
    return reverse("api:v1:hackathon_detail", kwargs={"pk": hackathon.pk})


@pytest.fixture
def data(image_file, future_date, past_date):
    return {
        "title": "test hackathon",
        "description": "test hackathon",
        "prize": 1000,
        "image": image_file,
        "start_datetime": past_date,
        "end_datetime": future_date,
    }


@pytest.mark.django_db
class TestHackathonListCreateAPIView:

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
                ("post", status.HTTP_201_CREATED),
            ],
        )
        def test_host_user(
            self, api_client, host_user, list_url, data, method, expected_status_code
        ):
            api_client.force_authenticate(user=host_user)
            response = getattr(api_client, method)(list_url, data=data)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("post", status.HTTP_201_CREATED),
            ],
        )
        def test_admin(
            self, api_client, admin_user, list_url, data, method, expected_status_code
        ):
            api_client.force_authenticate(user=admin_user)
            response = getattr(api_client, method)(list_url, data=data)
            assert response.status_code == expected_status_code

    def test_perform_create(self, api_client, list_url, admin_user, data):
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(list_url, data=data)
        assert response.status_code == status.HTTP_201_CREATED

        hackathon_id = response.data["id"]
        hackathon = Hackathon.objects.get(pk=hackathon_id)
        assert hackathon.hosted_by == admin_user


@pytest.mark.django_db
class TestHackathonRetrieveUpdateDestroyAPIView:

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
            response = getattr(api_client, method)(detail_url, data={})
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
            self, api_client, user, detail_url, method, expected_status_code
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
        def test_host_but_not_hackathon_host(
            self, api_client, host_user, detail_url, data, method, expected_status_code
        ):
            api_client.force_authenticate(user=host_user)
            response = getattr(api_client, method)(detail_url, data={})
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
            self, api_client, hackathon, detail_url, data, method, expected_status_code
        ):
            api_client.force_authenticate(user=hackathon.hosted_by)
            response = getattr(api_client, method)(detail_url, data={})
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
            self, api_client, admin_user, detail_url, method, expected_status_code
        ):
            api_client.force_authenticate(user=admin_user)
            response = getattr(api_client, method)(detail_url, data={})
            assert response.status_code == expected_status_code
