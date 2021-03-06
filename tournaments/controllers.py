from random import shuffle

from .constants import SINGLE_ELIMINATION
from .models import Achievement
from .models import Match
from .models import Round
from .models import Stage


class BracketController:
    def __init__(self, tournament):
        self.tournament = tournament
        self.matches = Match.objects.filter(round__stage__tournament=self.tournament)
        self.stage = Stage.objects.get(tournament=tournament)

    def build_bracket(self):
        if self.stage.format == SINGLE_ELIMINATION:
            return self._single_elimination()

    def start_tournament(self):
        first_round = Round.objects.get(first_round=True, stage=self.stage)
        participants = self.tournament.participants.all()
        shuffle(list(participants))
        for idx, team in enumerate(participants):
            if idx % 2 == 0:
                match = Match(
                    home_team=participants[idx],
                    away_team=participants[idx + 1],
                    round=first_round,
                )
                match.save()

    def _single_elimination(self):
        tournament_data = dict()
        rounds = Round.objects.filter(stage__tournament=self.tournament).order_by(
            'number',
        )
        for round in rounds:
            matches = Match.objects.filter(round=round).order_by('number')
            tournament_data[round] = list(matches)

        return tournament_data

    def save_loser_results(self, position, tournament, team):
        if position == 1:
            position = '1st'
        elif position == 2:
            position = '2nd'
        elif position == 3:
            position = '3rd'
        else:
            position = f'{position}/{position * 2}th'

        for player in self.members.filter(role='player'):
            Achievement.objects.create(
                position=position,
                tournament=tournament,
                team=team,
            )
