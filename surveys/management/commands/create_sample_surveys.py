from datetime import datetime

from django.core.management.base import BaseCommand

from surveys.tests.factories import basic_survey_structure, tight_survey_structure, pet_survey


class Command(BaseCommand):
    help = "Create sample surveys."

    def handle(self, *args, **options):
        basic_survey_structure("Long Text Survey")
        tight_survey_structure("Tight Structure Survey")
        pet_survey(f"Pet Survey {datetime.now()}")

        self.stdout.write(self.style.SUCCESS("Done"))
