from django import forms
from django.forms import ModelForm
from slugify import slugify

from .constants import STAGE_FORMAT_CHOICES
from .models import Stage
from .models import Tournament
from disciplines.models import Discipline
from organizations.models import Organization


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
        tournament.slug = slugify(tournament.name)
        stage_format = self.cleaned_data['format']
        if commit:
            tournament.save()
            stage = Stage(tournament=tournament, format=stage_format)
            stage.save()
        return tournament
