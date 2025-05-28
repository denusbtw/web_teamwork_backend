from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS

from web_teamwork.hackathons.models import Hackathon
from web_teamwork.hackathons.utils import (
    resolve_hackathon_id_from_view,
    resolve_hackathon_id_from_obj,
)


class IsHackathonHost(BasePermission):
    def has_permission(self, request, view):
        hackathon_id = resolve_hackathon_id_from_view(view)
        hackathon = get_object_or_404(Hackathon, pk=hackathon_id)
        return request.user.is_authenticated and request.user == hackathon.hosted_by

    def has_object_permission(self, request, view, obj):
        hackathon_id = resolve_hackathon_id_from_obj(obj)
        hackathon = get_object_or_404(Hackathon, pk=hackathon_id)
        return request.user.is_authenticated and request.user == hackathon.hosted_by


class ParticipantCanDeleteSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method == "DELETE" and obj.user == request.user
