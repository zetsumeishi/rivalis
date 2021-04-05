from django import template
from django.utils import timezone

register = template.Library()


@register.filter(name='tournament_status')
def tournament_status(tournament):
    if tournament.start_date >= timezone.now():
        return 'Upcoming'
    else:
        return 'Ongoing or Finished'
