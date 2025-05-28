from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth import get_user_model

from web_teamwork.hackathons.models import Participant

User = get_user_model()


class IsHost(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_host


def resolve_user_id_from_obj(obj):
    match obj:
        case User():
            return obj.pk
        case Participant():
            return obj.user_id
        case _:
            return None


class IsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_id = resolve_user_id_from_obj(obj)
        return request.user.is_authenticated and request.user.pk == user_id
