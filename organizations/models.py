from django.db import models

from disciplines.models import Discipline
from users.models import User


class Organization(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    description = models.TextField()
    is_business = models.BooleanField(default=False)
    twitch = models.URLField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    members = models.ManyToManyField(User, through='TeamMembership')
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TeamMembership(models.Model):
    role = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.email} | {self.team.name} | {self.role}'