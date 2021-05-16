from django.shortcuts import render

from tournaments.models import Tournament


def home(request):
    upcoming_tournaments = Tournament.objects.all().order_by('-start_date')[:4]
    context = {
        'upcoming_tournaments': upcoming_tournaments,
    }
    return render(request, 'www/home.html', context)
