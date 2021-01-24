from django import template

register = template.Library()


@register.filter(name='team_owner')
def team_owner(user, team):
    """Custom templatetag that evaluates if the logged user is the owner of the team.

    Args:
        user: Current authenticated user.
        team: Team object from the detail_team view.

    Returns:
        True if the current user is the owner of the team's organization.
    """
    return team.organization.owner == user
