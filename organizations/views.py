from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from slugify import slugify

from .forms import OrganizationForm
from .forms import TeamForm
from .models import Organization
from .models import Team


@login_required
def create_organization(request):
    context = dict()
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            is_business = form.cleaned_data['is_business']
            twitch = form.cleaned_data['twitch']
            context['organization'] = Organization.objects.create(
                name=name,
                slug=slugify(name),
                description=description,
                is_business=is_business,
                twitch=twitch,
                owner=request.user,
            )
            return render(request, 'organizations/detail.html', context)
    context['form'] = OrganizationForm()
    return render(request, 'organizations/create.html', context)


def detail_organization(request, organization_slug):
    context = dict()
    context['organization'] = Organization.objects.get(slug=organization_slug)
    context['teams'] = Team.objects.filter(organization=context['organization'])
    return render(request, 'organizations/detail.html', context)


@login_required
def create_team(request):
    context = dict()
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            discipline = form.cleaned_data['discipline']
            organization = Organization.objects.get(owner=request.user)
            team = Team.objects.create(
                name=name,
                slug=slugify(name),
                discipline=discipline,
                organization=organization,
            )
            context = {'team': team}
            return render(request, 'teams/detail.html', context)
    context['form'] = TeamForm()
    return render(request, 'teams/create.html', context)


def detail_team(request, organization_slug, team_slug):
    context = dict()
    context['organization'] = Organization.objects.get(slug=organization_slug)
    context['team'] = Team.objects.filter(
        slug=team_slug,
        organization=context['organization'],
    )
    return render(request, 'teams/detail.html', context)
