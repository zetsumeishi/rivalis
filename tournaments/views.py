from django.shortcuts import render

from .models import Tournament


def tournaments(request):
    tournaments = Tournament.objects.all()

    context = {'tournaments': tournaments}
    return render(request, 'tournaments/tournaments.html', context)
