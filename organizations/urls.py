from django.urls import path

from . import views

app_name = 'organizations'

urlpatterns = [
    path('create-team/', views.create_team, name='create_team'),
    path('kick-team-member/', views.kick_team_member, name='kick_team_member'),
    path('create-organization/', views.create_organization, name='create_organization'),
    path('<str:organization_slug>/edit-organization/', views.edit_organization, name='edit_organization'),
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
