from django.db import models

from .constants import ACCEPTED
from .constants import REGION_CHOICES
from .constants import SIZE_CHOICES
from .constants import STAGE_FORMAT_CHOICES
from .constants import STATUS_CHOICES
from disciplines.models import Discipline
from organizations.models import Team


class Tournament(models.Model):
    # Fields
    description = models.TextField('Description', blank=True)
    is_registration_open = models.BooleanField(default=True)
    name = models.CharField('Name', max_length=255)
    prizes = models.TextField('Prizes', blank=True)
    region = models.CharField(
        'Region',
        max_length=5,
        choices=REGION_CHOICES,
        default='euw',
    )
    rules = models.TextField('Rules')
    size = models.IntegerField(
        'Size',
        choices=SIZE_CHOICES,
        default=4,
    )
    start_date = models.DateTimeField(auto_now_add=True)

    # Relationships
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    organizer = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='organizer',
    )
    non_profit = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='non_profit',
        null=True,
    )
    participants = models.ManyToManyField(Team, through='TournamentMembership')

    def __str__(self):
        return (
            f'{self.name} by {self.organizer.name} on {self.discipline} | {self.region}'
        )

    @property
    def is_full(self):
        tournament_memberships = TournamentMembership.objects.filter(
            tournament=self,
            status=ACCEPTED,
        ).count()
        return tournament_memberships == self.size

    @property
    def accepted_participants(self):
        return Team.objects.filter(
            tournamentmembership__status=ACCEPTED,
            tournament=self,
        )


class TournamentMembership(models.Model):
    status = models.CharField(
        'Status',
        max_length=12,
        choices=STATUS_CHOICES,
        default='waiting',
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tournament.name} | {self.team.name}'


class Stage(models.Model):
    # Fields
    format = models.CharField(
        'Format',
        max_length=32,
        choices=STAGE_FORMAT_CHOICES,
        default='single_elimination',
    )

    # Relationships
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    def __str__(self):
        return self.format


class Round(models.Model):
    # Fields
    first_round = models.BooleanField(default=False)
    name = models.CharField('Name', max_length=255)
    number = models.IntegerField(default=1)

    # Relationships
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Match(models.Model):
    # Fields
    away_score = models.IntegerField('Away score', null=True)
    home_score = models.IntegerField('Home score', null=True)

    # Relationships
    away_team = models.ForeignKey(
        Team,
        related_name='away_team',
        on_delete=models.CASCADE,
    )
    home_team = models.ForeignKey(
        Team,
        related_name='home_team',
        on_delete=models.CASCADE,
    )
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    number = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.home_team} VS {self.away_team}'


class Achievement(models.Model):
    position = models.PositiveSmallIntegerField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
