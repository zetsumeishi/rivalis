from django import forms
from slugify import slugify

from .models import Organization
from .models import Team
from .models import TeamMembership
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
            'organization',
        )

    discipline = forms.ModelChoiceField(
        queryset=Discipline.objects.all(),
        to_field_name='name',
        empty_label='Select a game',
    )
    organization = forms.ModelChoiceField(
        queryset=None,
        to_field_name='name',
        empty_label='Select an organization',
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.fields['organization'].queryset = Organization.objects.filter(
            owner=self.request.user,
        )

    def save(self, commit=True, owner=None):
        team = super().save(commit=False)
        team.slug = slugify(team.name)
        if commit:
            team.save()
            membership = TeamMembership(user=owner, team=team, role='owner')
            membership.save()
        return team
