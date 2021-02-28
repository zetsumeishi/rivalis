from django import template

from tournaments.models import TournamentMembership

register = template.Library()


@register.filter(name='team_status')
def team_status(team, tournament):
    """Custom templatetag that evaluates if the logged user is the owner of the team.

    Args:
        user: Current authenticated user.
        team: Team object from the detail_team view.

    Returns:
        True if the current user is the owner of the team's organization.
    """
    tournament_membership = TournamentMembership.objects.get(
        tournament=tournament,
        team=team,
    )
    return tournament_membership.status.title()
