from django import forms

from .models import Organization
from .models import Team
from disciplines.models import Discipline


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = (
            'name',
            'short_name',
            'description',
            'twitch',
        )


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = (
            'name',
            'discipline',
        )

    discipline = forms.ModelChoiceField(
        queryset=Discipline.objects.all(),
        to_field_name='name',
        empty_label='Select a game',
    )
