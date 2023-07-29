""" Script that generates a fixture in core/fixtures/core/test_fixture.json """

import os
import django
from random import choice, randint
from pathlib import Path
from faker.factory import Factory
from django.core import serializers

BASE_DIR = Path(__file__).resolve().parent.parent.parent
APP_DIR = BASE_DIR / "core"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", str(BASE_DIR / "d2rlld" / "settings"))
django.setup()

from core.models import *

Faker = Factory.create
fake = Faker()
fake.seed(0)


def generate_dummy_data(
    num_tournaments=10, num_participants=100, num_brackets=50, num_matches=200
):
    tournaments = []
    participants = []
    brackets = []
    matches = []

    for _ in range(num_tournaments):
        tournament = Tournament(
            name=fake.catch_phrase(),
            description=fake.paragraph(),
            start_date=fake.future_datetime(),
            end_date=fake.future_datetime(),
            organizer=choice(User.objects.all()),
            status=choice(["ongoing", "upcoming", "completed"]),
        )
        tournaments.append(tournament)

    for _ in range(num_participants):
        participant = Participant(
            tournament=choice(tournaments),
            player=choice(User.objects.all()),
        )
        participants.append(participant)

    for _ in range(num_brackets):
        bracket = Bracket(
            tournament=choice(tournaments),
            round_number=randint(1, 10),
            is_final=fake.boolean(),
        )
        brackets.append(bracket)

    for _ in range(num_matches):
        match = Match(
            bracket=choice(brackets),
            participant1=choice(participants),
            participant2=choice(participants),
            winner=choice(participants),
            is_completed=fake.boolean(),
        )
        matches.append(match)

    match_results = []
    for match in matches:
        result = MatchResult(
            match=match,
            result_description=fake.paragraph(),
        )
        match_results.append(result)

    # Serialize the data and save it to a fixture file
    all_objects = tournaments + participants + brackets + matches + match_results
    fixture_file = APP_DIR / "fixtures/core/test_fixture.json"
    with open(fixture_file, "w") as f:
        serializers.serialize("json", all_objects, indent=2, fp=f)

    print("Dummy data successfully generated.")


if __name__ == "__main__":
    generate_dummy_data(
        num_tournaments=10, num_participants=100, num_brackets=50, num_matches=200
    )
