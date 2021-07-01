from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from .constants import ACCEPTED
from .constants import REJECTED
from .controllers import BracketController
from .forms import MatchForm
from .forms import RegistrationForm
from .forms import TournamentForm
from .models import Match
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
                'tournament_id': tournament.id,
            }
            return redirect(reverse('tournaments:detail_tournament', kwargs=kwargs))
        else:
            messages.add_message(request, messages.ERROR, 'Mistakes were made')
    form = TournamentForm(request=request)
    context = {'form': form}
    return render(request, 'tournaments/create.html', context)


def detail_tournament(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    matches = Match.objects.filter(round__stage__tournament=tournament)
    tournament_data = dict()

    # Generate the bracket if the tournament has started and no match was created
    if not tournament.is_registration_open and matches:
        controller = BracketController(tournament)
        tournament_data = controller.build_bracket()

    tournament_membership = TournamentMembership.objects.filter(
        tournament__id=tournament.id,
    ).order_by('status')

    context = {
        'tournament': tournament,
        'tournament_data': tournament_data,
        'tournament_membership': tournament_membership,
    }
    return render(request, 'tournaments/detail.html', context)


def start_tournament(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    controller = BracketController(tournament)
    if tournament.is_registration_open:
        controller.start_tournament()
        tournament.is_registration_open = False
        tournament.save()
    tournament_data = controller.build_bracket()
    context = {
        'tournament': tournament,
        'tournament_data': tournament_data,
    }
    return render(request, 'tournaments/detail.html', context)


def tournament_registration(request, tournament_id):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request=request)
        if form.is_valid():
            form.save(tournament_id=tournament_id)
            kwargs = {
                'tournament_id': tournament_id,
            }
            return redirect(reverse('tournaments:detail_tournament', kwargs=kwargs))
        else:
            messages.add_message(request, messages.ERROR, 'Mistakes were made')
    form = RegistrationForm(request=request)
    context = {'form': form}
    return render(request, 'tournaments/register.html', context)


def tournaments(request):
    tournaments = Tournament.objects.all().order_by('start_date')

    context = {'tournaments': tournaments}
    return render(request, 'tournaments/tournaments.html', context)


def manage_tournament(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    context = {
        'tournament': tournament,
    }
    return render(request, 'tournaments/manage_tournament.html', context)


def reject_participant(request):
    if request.is_ajax():
        participant_id = request.GET.get('participant_id', None)
        tournament_id = request.GET.get('tournament_id', None)
        participant = Team.objects.get(id=int(participant_id))
        tournament_membership = TournamentMembership.objects.get(
            tournament__id=tournament_id,
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
        tournament_id = request.GET.get('tournament_id', None)
        participant = Team.objects.get(id=int(participant_id))
        tournament_membership = TournamentMembership.objects.get(
            tournament__id=tournament_id,
            team=participant,
        )
        tournament_membership.status = ACCEPTED
        tournament_membership.save(update_fields=['status'])
        response = {
            'id': str(participant_id),
        }
        return JsonResponse(response, status=200)
    return redirect(request.META.get('HTTP_REFERER'))


def match_detail(request, tournament_id, match_id):
    tournament = Tournament.objects.get(id=tournament_id)
    match = Match.objects.get(id=match_id)

    user_is_member = False
    if (
        request.user in match.home_team.members.all()
        and request.user in match.away_team.members.all()
    ):
        user_is_member = True

    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            form.save()
            kwargs = {
                'tournament_id': tournament_id,
                'match_id': match_id,
            }
            return redirect(reverse('tournaments:match_details', kwargs=kwargs))
        else:
            messages.add_message(request, messages.ERROR, 'Mistakes were made')

    score_already_added = match.home_score and match.away_score

    context = {
        'tournament': tournament,
        'match': match,
        'user_is_member': user_is_member,
        'score_already_added': score_already_added,
    }

    return render(request, 'tournaments/match_detail.html', context)


def match_results(request, tournament_id, match_id):
    tournament = Tournament.objects.get(id=tournament_id)
    match = Match.objects.get(id=match_id)

    if (
        request.user not in match.home_team.members.all()
        and request.user not in match.away_team.members.all()
    ):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            form.save()
            controller = BracketController(tournament)
            position = Match.objects.filter(round=match.round).count()
            if match.home_score > match.away_score:
                controller.save_loser_results(position, tournament, match.away_team)
            else:
                controller.save_loser_results(position, tournament, match.home_team)
            kwargs = {
                'tournament_id': tournament_id,
                'match_id': match_id,
            }
            return redirect(reverse('tournaments:match_details', kwargs=kwargs))
        else:
            messages.add_message(request, messages.ERROR, 'Mistakes were made')

    form = MatchForm()
    context = {
        'tournament': tournament,
        'match': match,
        'form': form,
    }
    return render(request, 'tournaments/match_results.html', context)
