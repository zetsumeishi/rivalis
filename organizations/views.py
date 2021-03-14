from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from .decorators import is_owner
from .forms import EditOrganizationForm
from .forms import OrganizationForm
from .forms import TeamForm
from .models import Organization
from .models import Team
from users.models import User


@is_owner
@login_required
def edit_organization(request, organization_slug):
    """User profile view

    This view is used for handling GET and POST request to display and update the
    user.
    """
    organization = Organization.objects.get(slug=organization_slug)
    if request.method == 'POST':
        form = EditOrganizationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            kwargs = {
                'organization_slug': organization_slug,
            }
            messages.add_message(
                request,
                messages.SUCCESS,
                'Organization updated successfully',
            )
            return redirect(reverse('organizations:detail_organization', kwargs=kwargs))
        else:
            messages.add_message(request, messages.ERROR, 'Mistakes were made')

    form_data = {
        'name': organization.name,
        'short_name': organization.short_name,
        'description': organization.description,
        'logo': organization.logo,
        'website': organization.website,
        'twitch': organization.twitch,
        'twitter': organization.twitter,
        'reddit': organization.reddit,
        'instagram': organization.instagram,
        'youtube': organization.youtube,
    }
    context = {
        'form': EditOrganizationForm(initial=form_data),
    }
    return render(request, 'organizations/edit_organization.html', context)


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
