from django.urls import path
from .views import (
    HomeView,
    ProfileView,
    TournamentCreateView,
    TournamentUpdateView,
    TournamentDeleteView,
    ParticipantRegistrationView,
    ParticipantListView,
    TournamentBracketsView,
    MatchResultsView,
    TournamentStandingsView,
    MatchHistoryView,
    SpectatorView,
    UserProfileView,
    TournamentArchiveView,
)

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path(
        "tournament/create/", TournamentCreateView.as_view(), name="tournament-create"
    ),
    path(
        "tournament/<int:tournament_id>/update/",
        TournamentUpdateView.as_view(),
        name="tournament-update",
    ),
    path(
        "tournament/<int:tournament_id>/delete/",
        TournamentDeleteView.as_view(),
        name="tournament-delete",
    ),
    path(
        "tournament/<int:tournament_id>/register/",
        ParticipantRegistrationView.as_view(),
        name="participant-register",
    ),
    path(
        "tournament/<int:tournament_id>/participants/",
        ParticipantListView.as_view(),
        name="participant-list",
    ),
    path(
        "tournament/<int:tournament_id>/brackets/",
        TournamentBracketsView.as_view(),
        name="tournament-brackets",
    ),
    path(
        "tournament/<int:tournament_id>/results/",
        MatchResultsView.as_view(),
        name="match-results",
    ),
    path(
        "tournament/<int:tournament_id>/standings/",
        TournamentStandingsView.as_view(),
        name="tournament-standings",
    ),
    path(
        "tournament/<int:tournament_id>/history/",
        MatchHistoryView.as_view(),
        name="match-history",
    ),
    path(
        "tournament/<int:tournament_id>/spectate/",
        SpectatorView.as_view(),
        name="spectator-view",
    ),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("archive/", TournamentArchiveView.as_view(), name="tournament-archive"),
]
