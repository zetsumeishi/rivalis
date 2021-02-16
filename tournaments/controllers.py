from .constants import DOUBLE_ELIMINATION
from .constants import NB_MATCHES_PER_ROUND_LB
from .constants import SINGLE_ELIMINATION
from .constants import SIZES_ROUNDS
from .models import Match
from .models import Stage


class BracketController:
    def __init__(self, tournament):
        self.tournament = tournament
        self.matches = Match.objects.filter(round__stage__tournament=self.tournament)
        self.stage = Stage.objects.get(tournament=tournament)

    def build_bracket(self, empty=False):
        if self.stage.format == SINGLE_ELIMINATION:
            return self._single_elimination(empty=empty)
        if self.stage.format == DOUBLE_ELIMINATION:
            return self._double_elimination(empty=empty)

    def _single_elimination(self, empty=False):
        nb_rounds = SIZES_ROUNDS[self.tournament.size]
        if not self.matches or empty:
            teams_js = [['', ''] for i in range(int(self.tournament.size / 2))]
            results_js = [[] for i in range(nb_rounds)]
        else:
            teams_js = [
                [match.home_team.name, match.away_team.name]
                for match in self.matches.filter(round__number=1)
            ]
            results_js = [[] for i in range(nb_rounds)]

            for i in range(nb_rounds):
                round_matches = self.matches.filter(round__number=i + 1)
                for match in round_matches:
                    results_js[i].append([match.home_score, match.away_score])
        return teams_js, results_js

    def _double_elimination(self, empty=False):
        nb_rounds = SIZES_ROUNDS[self.tournament.size]
        if not self.matches or empty:
            teams_js = [['', ''] for i in range(int(self.tournament.size / 2))]
            # Generate an empty WB
            winner_bracket = []
            nb_matches = self.tournament.size
            for i in range(nb_rounds, 0, -1):
                round_matches = []
                nb_matches = int(nb_matches / 2)
                for j in range(nb_matches, 0, -1):
                    round_matches.append([0, 0])
                winner_bracket.append(round_matches)

            # Generate an empty LB
            loser_bracket = []
            nb_participants = self.tournament.size
            for i in range(nb_rounds, 0, -1):
                round_matches = []
                nb_matches = NB_MATCHES_PER_ROUND_LB[nb_participants]
                for j in range(nb_matches, 0, -1):
                    round_matches.append([0, 0])
                loser_bracket.append(round_matches)
                nb_participants = int(nb_participants / 2)

            results_js = [winner_bracket, loser_bracket]
        else:
            pass
        return teams_js, results_js
