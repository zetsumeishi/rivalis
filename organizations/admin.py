from django.contrib import admin

from .models import Organization
from .models import Team
from .models import TeamMembership

admin.site.register(Organization)
admin.site.register(Team)
admin.site.register(TeamMembership)
