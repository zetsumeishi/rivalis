import subprocess

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError


class Command(BaseCommand):
    help = 'Deletes .pyc, __pycache__ files'

    def handle(self, *args, **options):
        try:
            subprocess.Popen('py3clean .', shell=True, stdout=subprocess.PIPE)
        except Exception as e:
            raise CommandError(f"Couldn't execute clean_pyc.\n{e}")

        self.stdout.write(
            self.style.SUCCESS('Successfully deleted all .pyc and __pycache__  files.'),
        )
