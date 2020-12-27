import subprocess

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError


class Command(BaseCommand):
    help = 'Deletes migrations files'

    def handle(self, *args, **options):
        try:
            subprocess.Popen(
                (
                    'find . -path "*/migrations/*.py" -not -name "__init__.py" '
                    '-not -path "*env*" -delete'
                ),
                shell=True,
                stdout=subprocess.PIPE,
            )
            subprocess.Popen(
                'find . -path "*/migrations/*.pyc" -not -path "*env*" -delete',
                shell=True,
                stdout=subprocess.PIPE,
            )
        except Exception as e:
            raise CommandError(f"Couldn't execute del_mig.\n{e}")

        self.stdout.write(
            self.style.SUCCESS('Successfully deleted all migrations files.'),
        )
