from datetime import timedelta
from io import BytesIO

import pytest
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from web_teamwork.hackathons.tests.factories import (
    CategoryFactory,
    HackathonFactory,
    ParticipantFactory,
)
from web_teamwork.users.tests.factories import UserFactory

User = get_user_model()


@pytest.fixture
def now():
    return timezone.now()


@pytest.fixture
def future_date(now):
    return now + timedelta(days=7)


@pytest.fixture
def past_date(now):
    return now - timedelta(days=7)


@pytest.fixture
def image_file():
    buffer = BytesIO()
    Image.new("RGB", (100, 100)).save(buffer, format="PNG")
    buffer.seek(0)
    return SimpleUploadedFile("test.png", buffer.read(), content_type="image/png")


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user_factory():
    return UserFactory


@pytest.fixture
def category_factory():
    return CategoryFactory


@pytest.fixture
def category(category_factory):
    return category_factory()


@pytest.fixture
def hackathon_factory():
    return HackathonFactory


@pytest.fixture
def hackathon(hackathon_factory):
    return hackathon_factory()


@pytest.fixture
def participant_factory():
    return ParticipantFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(user_factory):
    return user_factory(role=User.Role.USER)


@pytest.fixture
def host_user(user_factory):
    return user_factory(role=User.Role.HOST)


@pytest.fixture
def participant(hackathon, participant_factory):
    return participant_factory(hackathon=hackathon)
