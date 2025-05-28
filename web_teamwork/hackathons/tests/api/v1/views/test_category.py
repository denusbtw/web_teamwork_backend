import pytest
from django.urls import reverse
from rest_framework import status


@pytest.fixture
def list_url():
    return reverse("api:v1:category_list")


@pytest.fixture
def detail_url(category):
    return reverse("api:v1:category_detail", kwargs={"pk": category.pk})


@pytest.fixture
def data():
    return {"title": "test category"}


@pytest.mark.django_db
class TestCategoryListCreateAPIView:

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
        def test_host_user(
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
        def test_admin_user(
            self, api_client, admin_user, list_url, data, method, expected_status_code
        ):
            api_client.force_authenticate(user=admin_user)
            response = getattr(api_client, method)(list_url, data=data)
            assert response.status_code == expected_status_code


@pytest.mark.django_db
class TestCategoryRetrieveUpdateDestroyAPIView:

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
        def test_host_user(
            self, api_client, host_user, detail_url, method, expected_status_code
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
        def test_admin_user(
            self, api_client, admin_user, detail_url, data, method, expected_status_code
        ):
            api_client.force_authenticate(user=admin_user)
            response = getattr(api_client, method)(detail_url, data={})
            assert response.status_code == expected_status_code
