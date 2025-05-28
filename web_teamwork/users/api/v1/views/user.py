from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from web_teamwork.core.api.v1.permissions import ReadOnly
from web_teamwork.users.api.v1.permissions import IsSelf
from web_teamwork.users.api.v1.serializers import (
    UserDetailSerializer,
    UserUpdateSerializer,
    UserListSerializer,
    UserCreateSerializer,
)

User = get_user_model()


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return UserListSerializer
        return UserCreateSerializer


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [ReadOnly | permissions.IsAdminUser | IsSelf]

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return UserDetailSerializer
        return UserUpdateSerializer


class UserMeAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return UserDetailSerializer
        return UserUpdateSerializer
