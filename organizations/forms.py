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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Name'})
        self.fields['short_name'].widget.attrs.update({'placeholder': 'Short name'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Description'})
        self.fields['twitch'].widget.attrs.update({'placeholder': 'Twitch URL'})

    def save(self, commit=True, owner=None):
        organization = super().save(commit=False)
        organization.slug = slugify(organization.name)
        organization.owner = owner
        if commit:
            organization.save()
        return organization


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
        self.fields['name'].widget.attrs.update({'placeholder': 'Name'})

    def save(self, commit=True, owner=None):
        team = super().save(commit=False)
        team.slug = slugify(team.name)
        if commit:
            team.save()
            membership = TeamMembership(user=owner, team=team, role='owner')
            membership.save()
        return team
