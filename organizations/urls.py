from django.urls import path

from . import views

app_name = 'organizations'

urlpatterns = [
    path('create-team/', views.create_team, name='create_team'),
    path('create-organization/', views.create_organization, name='create_organization'),
    path('kick-team-member/', views.kick_team_member, name='kick_team_member'),
    path(
        '<str:organization_slug>/',
        views.detail_organization,
        name='detail_organization',
    ),
    path(
        '<str:organization_slug>/teams/<str:team_slug>/',
        views.detail_team,
        name='detail_team',
    ),
]
