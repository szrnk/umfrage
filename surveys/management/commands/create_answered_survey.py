from django.core.management.base import BaseCommand

from surveys.tests.factories import create_answered_survey


class Command(BaseCommand):
    help = "Create sample surveys."

    def handle(self, *args, **options):
        for i in range(10):
            create_answered_survey()
        self.stdout.write(self.style.SUCCESS("Done"))
