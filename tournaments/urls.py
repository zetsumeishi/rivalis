from django.urls import path

from . import views

app_name = 'tournaments'

urlpatterns = [
    path('tournaments/', views.tournaments, name='tournaments'),
    path('create-tournament/', views.create_tournament, name='create_tournament'),
    path('reject-participant/', views.reject_participant, name='reject_participant'),
    path('accept-participant/', views.accept_participant, name='accept_participant'),
    path(
        'tournament/<int:tournament_id>/registration',
        views.tournament_registration,
        name='tournament_registration',
    ),
    path(
        'tournament/<int:tournament_id>/manage',
        views.manage_tournament,
        name='manage_tournament',
    ),
    path(
        'tournament/<int:tournament_id>/',
        views.detail_tournament,
        name='detail_tournament',
    ),
    path(
        'start-tournament/<int:tournament_id>',
        views.start_tournament,
        name='start_tournament',
    ),
    path(
        'tournament/<int:tournament_id>/match/<int:match_id>',
        views.match_detail,
        name='match_detail',
    ),
]
