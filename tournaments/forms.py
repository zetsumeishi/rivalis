from django import forms
from django.forms import Form
from django.forms import ModelForm

from .constants import SIZES_ROUNDS
from .constants import STAGE_FORMAT_CHOICES
from .constants import WAITING
from .models import Round
from .models import Stage
from .models import Tournament
from .models import TournamentMembership
from disciplines.models import Discipline
from organizations.models import Organization
from organizations.models import Team


class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = [
            'name',
            'region',
            'size',
            'description',
            'prizes',
            'rules',
            'discipline',
            'organizer',
        ]

    discipline = forms.ModelChoiceField(
        queryset=Discipline.objects.all(),
        to_field_name='name',
        empty_label='Select a game',
    )
    organizer = forms.ModelChoiceField(
        queryset=None,
        to_field_name='name',
        empty_label='Select an organization',
    )
    format = forms.ChoiceField(choices=STAGE_FORMAT_CHOICES)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.fields['organizer'].queryset = Organization.objects.filter(
            owner=self.request.user,
        )
        self.fields['name'].widget.attrs.update({'placeholder': 'Name'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Description'})
        self.fields['size'].widget.attrs.update(
            {'placeholder': 'Number of participants'},
        )
        self.fields['prizes'].widget.attrs.update({'placeholder': 'Prizes'})
        self.fields['rules'].widget.attrs.update({'placeholder': 'Rules'})

    def save(self, commit=True):
        tournament = super().save(commit=False)
        stage_format = self.cleaned_data['format']
        if commit:
            tournament.save()
            stage = Stage(tournament=tournament, format=stage_format)
            stage.save()
            self._generate_rounds(tournament, stage)
        return tournament

    def _generate_rounds(self, tournament, stage):
        for round_number in range(SIZES_ROUNDS[tournament.size] + 1):
            first_round = False
            if round_number == 1:
                round_name = 'Finals'
                first_round = True
            elif round_number == 2:
                round_name = 'Semifinals'
            elif round_number == 3:
                round_name = 'Quarterfinals'
            else:
                round_name = f'Round {round_number}'
            new_round = Round(
                name=round_name,
                first_round=first_round,
                number=round_number,
                stage=stage,
            )
            new_round.save()


class RegistrationForm(Form):
    team = forms.ModelChoiceField(
        queryset=None,
        to_field_name='name',
        empty_label='Select a team',
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.fields['team'].queryset = Team.objects.filter(
            members__email=self.request.user.email,
        )

    def save(self, commit=True, tournament_id=None):
        tournament = Tournament.objects.get(id=tournament_id)
        data = {
            'tournament_id': tournament,
            'user': self.request.user,
            'status': WAITING,
        }
        team_registration = TournamentMembership(**data)
        team_registration.save()
        return tournament
