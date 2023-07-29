from django.db import models

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission


User = get_user_model()

# manager_group, created = Group.objects.get_or_create(name="Tournament Manager")

codenames = [
    "add_tournament",
    "change_tournament",
    "delete_tournament",
    "add_participant",
    "change_participant",
    "delete_participant",
    "add_match",
    "change_match",
    "delete_match",
]

# permissions = [Permission.objects.get(codename=name) for name in codenames]
# manager_group.permissions.add(permissions)


class Tournament(models.Model):
    STATUS_CHOICES = [
        ("ongoing", "Ongoing"),
        ("upcoming", "Upcoming"),
        ("completed", "Completed"),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="upcoming")

    def __str__(self):
        return self.name


class Participant(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tournament.name} - {self.player.username}"


class Bracket(models.Model):
    tournament = models.ForeignKey("Tournament", on_delete=models.CASCADE)
    round_number = models.PositiveIntegerField()
    is_final = models.BooleanField(default=False)

    def __str__(self):
        return f"Tournament: {self.tournament.name} - Round {self.round_number}"


class Match(models.Model):
    bracket = models.ForeignKey(Bracket, on_delete=models.CASCADE)
    participant1 = models.ForeignKey(
        Participant, related_name="participant1_matches", on_delete=models.CASCADE
    )
    participant2 = models.ForeignKey(
        Participant, related_name="participant2_matches", on_delete=models.CASCADE
    )
    winner = models.ForeignKey(
        Participant,
        related_name="winner_matches",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Match in Bracket: {self.bracket} - {self.participant1} vs. {self.participant2}"


class MatchResult(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE)
    result_description = models.TextField()

    def __str__(self):
        return f"Result of Match: {self.match}"
