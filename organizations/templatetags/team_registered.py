from django import template

register = template.Library()


@register.filter(name='team_registered')
def team_registered(team, tournament):
    return team in tournament.participants.all()
