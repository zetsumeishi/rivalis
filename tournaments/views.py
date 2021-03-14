from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from .constants import ACCEPTED
from .constants import REJECTED
from .controllers import BracketController
from .forms import RegistrationForm
from .forms import TournamentForm
from .models import Tournament
from .models import TournamentMembership
from organizations.models import Team


@login_required
def create_tournament(request):
    """User profile view

    This view is used for handling GET and POST request to display and update the
    user.
    """
    if request.method == 'POST':
        form = TournamentForm(request.POST, request=request)
        if form.is_valid():
            tournament = form.save()
            kwargs = {
                'tournament_slug': tournament.slug,
            }
            return redirect(reverse('tournaments:detail_tournament', kwargs=kwargs))
        else:
            messages.add_message(request, messages.ERROR, 'Mistakes were made')
    form = TournamentForm(request=request)
    context = {'form': form}
    return render(request, 'tournaments/create.html', context)


def detail_tournament(request, tournament_slug):
    tournament = Tournament.objects.get(slug=tournament_slug)
    empty = tournament.registration_is_open
    controller = BracketController(tournament)
    teams_js, results_js = controller.build_bracket(empty=empty)
    context = {
        'tournament': tournament,
        'teams_js': teams_js,
        'results_js': results_js,
    }
    return render(request, 'tournaments/detail.html', context)


def tournament_registration(request, tournament_slug):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request=request)
        if form.is_valid():
            form.save(tournament_slug=tournament_slug)
            kwargs = {
                'tournament_slug': tournament_slug,
            }
            return redirect(reverse('tournaments:detail_tournament', kwargs=kwargs))
        else:
            messages.add_message(request, messages.ERROR, 'Mistakes were made')
    form = RegistrationForm(request=request)
    context = {'form': form}
    return render(request, 'tournaments/register.html', context)


def tournaments(request):
    tournaments = Tournament.objects.all()

    context = {'tournaments': tournaments}
    return render(request, 'tournaments/tournaments.html', context)


def manage_tournament(request, tournament_slug):
    tournament = Tournament.objects.get(slug=tournament_slug)
    context = {
        'tournament': tournament,
    }
    return render(request, 'tournaments/manage_tournament.html', context)


def reject_participant(request):
    if request.is_ajax():
        participant_id = request.GET.get('participant_id', None)
        tournament_slug = request.GET.get('tournament_slug', None)
        participant = Team.objects.get(pk=int(participant_id))
        tournament_membership = TournamentMembership.objects.get(
            tournament__slug=tournament_slug,
            team=participant,
        )
        tournament_membership.status = REJECTED
        tournament_membership.save(update_fields=['status'])
        response = {
            'id': str(participant_id),
        }
        return JsonResponse(response, status=200)
    return redirect(request.META.get('HTTP_REFERER'))


def accept_participant(request):
    if request.is_ajax():
        participant_id = request.GET.get('participant_id', None)
        tournament_slug = request.GET.get('tournament_slug', None)
        participant = Team.objects.get(pk=int(participant_id))
        tournament_membership = TournamentMembership.objects.get(
            tournament__slug=tournament_slug,
            team=participant,
        )
        tournament_membership.status = ACCEPTED
        tournament_membership.save(update_fields=['status'])
        response = {
            'id': str(participant_id),
        }
        return JsonResponse(response, status=200)
    return redirect(request.META.get('HTTP_REFERER'))
