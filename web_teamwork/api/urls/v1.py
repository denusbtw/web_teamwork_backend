from django.urls import path

from web_teamwork.core.api.v1.views import LeaderboardAPIView
from web_teamwork.hackathons.api.v1.views import (
    HackathonListCreateAPIView,
    HackathonRetrieveUpdateDestroyAPIView,
    HackathonParticipantListCreateAPIView,
    HackathonParticipantRetrieveUpdateDestroyAPIView,
    CategoryListCreateAPIView,
    CategoryRetrieveUpdateDestroyAPIView,
)
from web_teamwork.users.api.v1.views import (
    UserListCreateAPIView,
    UserRetrieveUpdateDestroyAPIView,
    UserParticipantListAPIView,
    UserParticipantRetrieveDestroyAPIView,
)
from web_teamwork.users.api.v1.views.user import UserMeAPIView

app_name = "v1"
urlpatterns = [
    path("hackathons/", HackathonListCreateAPIView.as_view(), name="hackathon_list"),
    path(
        "hackathons/<uuid:pk>/",
        HackathonRetrieveUpdateDestroyAPIView.as_view(),
        name="hackathon_detail",
    ),
    path(
        "hackathons/<uuid:hackathon_id>/participants/",
        HackathonParticipantListCreateAPIView.as_view(),
        name="participant_list",
    ),
    path(
        "hackathons/<uuid:hackathon_id>/participants/<uuid:pk>/",
        HackathonParticipantRetrieveUpdateDestroyAPIView.as_view(),
        name="participant_detail",
    ),
    path("categories/", CategoryListCreateAPIView.as_view(), name="category_list"),
    path(
        "categories/<uuid:pk>/",
        CategoryRetrieveUpdateDestroyAPIView.as_view(),
        name="category_detail",
    ),
    path("users/", UserListCreateAPIView.as_view(), name="user_list"),
    path(
        "users/<uuid:pk>/",
        UserRetrieveUpdateDestroyAPIView.as_view(),
        name="user_detail",
    ),
    path("users/me/", UserMeAPIView.as_view(), name="user_me"),
    path(
        "users/<uuid:user_id>/participants/",
        UserParticipantListAPIView.as_view(),
        name="user_participant_list",
    ),
    path(
        "users/<uuid:user_id>/participants/<uuid:pk>/",
        UserParticipantRetrieveDestroyAPIView.as_view(),
        name="user_participant_detail",
    ),
    path("leaderboard/", LeaderboardAPIView.as_view(), name="leaderboard"),
]
