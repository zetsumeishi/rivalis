from django.urls import path

from . import views

app_name = 'tournaments'

urlpatterns = [
    path('tournaments/', views.tournaments, name='tournaments'),
    path('create-tournament/', views.create_tournament, name='create_tournament'),
    path('reject-participant/', views.reject_participant, name='reject_participant'),
    path('accept-participant/', views.accept_participant, name='accept_participant'),
    path(
        'tournament/<str:tournament_slug>/registration',
        views.tournament_registration,
        name='tournament_registration',
    ),
    path(
        'tournament/<str:tournament_slug>/manage',
        views.manage_tournament,
        name='manage_tournament',
    ),
    path(
        'tournament/<str:tournament_slug>/',
        views.detail_tournament,
        name='detail_tournament',
    ),
]
