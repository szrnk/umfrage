from django.core.management.base import BaseCommand

from surveys.tests.factories import pet_survey, interest_survey
from datetime import datetime


class Command(BaseCommand):
    help = "Create pet survey."

    # def add_arguments(self, parser):
    #     parser.add_argument('sample', nargs='+')

    def handle(self, *args, **options):
        pet_survey(f"Pet Survey {datetime.now()}")
        interest_survey(f"Interest Survey {datetime.now()}")
        self.stdout.write(self.style.SUCCESS("Done"))
