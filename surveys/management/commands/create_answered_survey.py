from django.core.management.base import BaseCommand

from surveys.tests.factories import create_answered_survey


class Command(BaseCommand):
    help = "Create answered surveys."

    def handle(self, *args, **options):
        N = 1
        surveys = [create_answered_survey().id for i in range(N)]
        self.stdout.write(self.style.SUCCESS(f"Done - created {N} - {surveys}"))
