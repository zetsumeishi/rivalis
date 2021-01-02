from django.db import models


class Discipline(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255, blank=True)
    editor_name = models.TextField()
    editor_website = models.URLField()

    def __str__(self):
        return f'{self.name} | {self.editor_name}'
