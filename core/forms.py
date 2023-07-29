from django import forms
from .models import Tournament, Participant, MatchResult


class TournamentCreationForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = "__all__"


class TournamentUpdateForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = "__all__"


class ParticipantRegistrationForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = "__all__"


class MatchResultsForm(forms.ModelForm):
    class Meta:
        model = MatchResult
        fields = "__all__"
