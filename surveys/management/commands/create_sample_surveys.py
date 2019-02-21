from datetime import datetime

from django.core.management.base import BaseCommand

from surveys.tests.factories import several_long_surveys, several_tight_surveys, pet_survey, interest_survey


class Command(BaseCommand):
    help = "Create sample surveys."

    def handle(self, *args, **options):
        several_long_surveys("Long Text Survey")
        several_tight_surveys("Tight Structure Survey")
        pet_survey(f"Pet Survey {datetime.now()}")
        interest_survey(f"Interest Survey {datetime.now()}")
        self.stdout.write(self.style.SUCCESS("Done"))
