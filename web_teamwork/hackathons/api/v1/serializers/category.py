from rest_framework import serializers

from web_teamwork.hackathons.models import Category


class BaseCategoryReadSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    slug = serializers.CharField()


class CategoryListSerializer(BaseCategoryReadSerializer):
    pass


class CategoryDetailSerializer(BaseCategoryReadSerializer):
    pass


class BaseCategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("title",)


class CategoryCreateSerializer(BaseCategoryWriteSerializer):
    pass


class CategoryUpdateSerializer(BaseCategoryWriteSerializer):
    class Meta(BaseCategoryWriteSerializer.Meta):
        extra_kwargs = {"title": {"required": False}}
