from django import template

from organizations.models import TeamMembership

register = template.Library()


@register.filter(name='member_role')
def member_role(user, team):
    """Custom templatetag that returns the player role.

    Args:
        user: User object that represents a member of the current user team.
        team: Current user Team object

    Returns:
        role: The role of the team member
    """
    team_membership = TeamMembership.objects.get(team=team, user=user)
    role = team_membership.role.title()
    return role
