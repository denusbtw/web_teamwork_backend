import pytest

from web_teamwork.hackathons.api.v1.serializers import CategoryUpdateSerializer


@pytest.mark.django_db
class TestCategoryUpdateSerializer:

    def test_no_error_if_empty_data(self, category_factory):
        category = category_factory()
        serializer = CategoryUpdateSerializer(category, data={})
        assert serializer.is_valid(), serializer.errors
