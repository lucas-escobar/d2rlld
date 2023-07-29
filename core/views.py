from django.shortcuts import render

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from .models import Tournament, Participant, Match
from .forms import (
    TournamentCreationForm,
    TournamentUpdateForm,
    ParticipantRegistrationForm,
    MatchResultsForm,
)


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tournaments"] = Tournament.objects.filter(
            status__in=["ongoing", "upcoming"]
        )
        return context


class ProfileView(TemplateView):
    template_name = "core/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


# View for creating a new tournament (for authorized users like admins or organizers)
class TournamentCreateView(View):
    def get(self, request):
        # Display the tournament creation form
        return render(
            request, "core/create_tournament.html", {"form": TournamentCreationForm()}
        )

    def post(self, request):
        # Handle the form submission and create the new tournament
        form = TournamentCreationForm(request.POST)
        if form.is_valid():
            tournament = form.save()
            return redirect("core/tournament-detail", tournament_id=tournament.id)
        return render(request, "create_tournament.html", {"form": form})


# View for updating an existing tournament (for authorized users)
class TournamentUpdateView(View):
    def get(self, request, tournament_id):
        # Display the tournament update form with the current tournament details
        tournament = Tournament.objects.get(id=tournament_id)
        return render(
            request,
            "core/update_tournament.html",
            {"form": TournamentUpdateForm(instance=tournament)},
        )

    def post(self, request, tournament_id):
        # Handle the form submission and update the existing tournament
        tournament = Tournament.objects.get(id=tournament_id)
        form = TournamentUpdateForm(request.POST, instance=tournament)
        if form.is_valid():
            tournament = form.save()
            return redirect("tournament-detail", tournament_id=tournament.id)
        return render(request, "core/update_tournament.html", {"form": form})


# View for deleting a tournament (for authorized users)
class TournamentDeleteView(View):
    def post(self, request, tournament_id):
        # Delete the specified tournament and redirect to the home page
        tournament = Tournament.objects.get(id=tournament_id)
        tournament.delete()
        return redirect("home")


# View for participant registration in a tournament
class ParticipantRegistrationView(View):
    def get(self, request, tournament_id):
        # Display the participant registration form for the specified tournament
        return render(
            request,
            "core/participant_registration.html",
            {"form": ParticipantRegistrationForm()},
        )

    def post(self, request, tournament_id):
        # Handle the form submission and register the participant for the tournament
        form = ParticipantRegistrationForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.tournament = Tournament.objects.get(id=tournament_id)
            participant.save()
            return redirect("tournament-detail", tournament_id=tournament_id)
        return render(request, "core/participant_registration.html", {"form": form})


# View for displaying the list of participants in a tournament
class ParticipantListView(View):
    def get(self, request, tournament_id):
        # Retrieve and display the list of participants for the specified tournament
        tournament = Tournament.objects.get(id=tournament_id)
        participants = Participant.objects.filter(tournament=tournament)
        return render(
            request,
            "core/participant_list.html",
            {"tournament": tournament, "participants": participants},
        )


# View for displaying the tournament brackets
class TournamentBracketsView(View):
    def get(self, request, tournament_id):
        # Generate and display the tournament brackets based on the tournament ID
        # The brackets can be dynamically generated based on the tournament's format and participants
        return render(request, "core/brackets.html", {"brackets": generated_brackets})


# View for reporting match results
class MatchResultsView(View):
    def get(self, request, tournament_id):
        # Display the match results form for the specified tournament
        return render(request, "core/match_results.html", {"form": MatchResultsForm()})

    def post(self, request, tournament_id):
        # Handle the form submission and record the match results
        form = MatchResultsForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.tournament = Tournament.objects.get(id=tournament_id)
            match.save()
            return redirect("tournament-detail", tournament_id=tournament_id)
        return render(request, "core/match_results.html", {"form": form})


# View for displaying the tournament standings and rankings
class TournamentStandingsView(View):
    def get(self, request, tournament_id):
        # Calculate and display the current standings and rankings for the specified tournament
        tournament = Tournament.objects.get(id=tournament_id)
        standings = calculate_standings(tournament)
        return render(
            request,
            "core/standings.html",
            {"tournament": tournament, "standings": standings},
        )


# View for displaying the match history for completed tournaments
class MatchHistoryView(View):
    def get(self, request, tournament_id):
        # Retrieve and display the match history for the specified completed tournament
        tournament = Tournament.objects.get(id=tournament_id)
        matches = Match.objects.filter(tournament=tournament, is_completed=True)
        return render(
            request,
            "core/match_history.html",
            {"tournament": tournament, "matches": matches},
        )


# View for allowing users to spectate ongoing matches
class SpectatorView(View):
    def get(self, request, tournament_id):
        # Display the ongoing matches for the specified tournament to the user as a spectator
        tournament = Tournament.objects.get(id=tournament_id)
        ongoing_matches = Match.objects.filter(
            tournament=tournament, is_completed=False
        )
        return render(
            request,
            "core/spectator_view.html",
            {"tournament": tournament, "matches": ongoing_matches},
        )


# View for user-specific profile information, achievements, etc.
class UserProfileView(View):
    def get(self, request):
        # Display user-specific information like registered tournaments, match history, etc.
        # Get the user's registered tournaments, match history, etc., from the database
        return render(request, "core/user_profile.html", {"user": request.user})


# View for archiving past tournaments and their details
class TournamentArchiveView(View):
    def get(self, request):
        # Retrieve and display past tournaments for reference and historical purposes
        past_tournaments = Tournament.objects.filter(status="completed")
        return render(
            request,
            "core/tournament_archive.html",
            {"past_tournaments": past_tournaments},
        )
