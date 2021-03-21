from django.urls import path

from . import views

app_name = 'organizations'

urlpatterns = [
    path('create-team/', views.create_team, name='create_team'),
    path('kick-team-member/', views.kick_team_member, name='kick_team_member'),
    path('create-organization/', views.create_organization, name='create_organization'),
    path(
        '<int:organization_id>/edit-organization/',
        views.edit_organization,
        name='edit_organization',
    ),
    path(
        '<int:organization_id>/',
        views.detail_organization,
        name='detail_organization',
    ),
    path(
        '<int:organization_id>/teams/<int:team_id>/',
        views.detail_team,
        name='detail_team',
    ),
]
