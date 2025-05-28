from rest_framework import generics, permissions

from web_teamwork.core.api.v1.permissions import ReadOnly
from web_teamwork.hackathons.api.v1.serializers import (
    CategoryListSerializer,
    CategoryCreateSerializer,
    CategoryDetailSerializer,
    CategoryUpdateSerializer,
)
from web_teamwork.hackathons.models import Category


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    permission_classes = [ReadOnly | permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return CategoryListSerializer
        return CategoryCreateSerializer


class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    permission_classes = [ReadOnly | permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return CategoryDetailSerializer
        return CategoryUpdateSerializer
