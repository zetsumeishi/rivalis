from django.shortcuts import render

from .controllers import BracketController
from .models import Tournament


def detail_tournament(request, tournament_slug):
    tournament = Tournament.objects.get(slug=tournament_slug)
    empty = not tournament.is_full and tournament.registration_is_open
    controller = BracketController(tournament)
    teams_js, results_js = controller.build_bracket(empty=empty)
    context = {
        'tournament': tournament,
        'teams_js': teams_js,
        'results_js': results_js,
    }
    return render(request, 'tournaments/detail.html', context)


def tournaments(request):
    tournaments = Tournament.objects.all()

    context = {'tournaments': tournaments}
    return render(request, 'tournaments/tournaments.html', context)
