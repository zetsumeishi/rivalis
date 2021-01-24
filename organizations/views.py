from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from .decorators import is_owner
from .forms import OrganizationForm
from .forms import TeamForm
from .models import Organization
from .models import Team
from users.models import User


@login_required
def kick_team_member(request):
    if request.is_ajax():
        member_id = request.GET.get('member_id', '')
        team_id = request.GET.get('team_id', '')
        member = User.objects.get(pk=int(member_id))
        team = Team.objects.get(pk=int(team_id))
        team.members.remove(member)
        response = {
            'id': str(member_id),
        }
        return JsonResponse(response, status=200)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def create_organization(request):
    context = dict()
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            organization = form.save(owner=request.user)
            kwargs = {'organization_slug': organization.slug}
            return redirect(reverse('organizations:detail_organization', kwargs=kwargs))
    context['form'] = OrganizationForm()
    return render(request, 'organizations/create.html', context)


def detail_organization(request, organization_slug):
    organization = Organization.objects.get(slug=organization_slug)
    teams = Team.objects.filter(organization=organization)

    context = {
        'organization': organization,
        'teams': teams,
    }
    return render(request, 'organizations/detail.html', context)


@login_required
@is_owner
def create_team(request):
    context = dict()
    if request.method == 'POST':
        form = TeamForm(request.POST, request=request)
        if form.is_valid():
            team = form.save(owner=request.user)
            kwargs = {
                'organization_slug': team.organization.slug,
                'team_slug': team.slug,
            }
            return redirect(reverse('organizations:detail_team', kwargs=kwargs))
    context['form'] = TeamForm(request=request)
    return render(request, 'teams/create.html', context)


def detail_team(request, organization_slug, team_slug):
    organization = Organization.objects.get(slug=organization_slug)
    team = Team.objects.get(
        slug=team_slug,
        organization=organization,
    )

    context = {
        'team': team,
        'organization': organization,
    }
    return render(request, 'teams/detail.html', context)
