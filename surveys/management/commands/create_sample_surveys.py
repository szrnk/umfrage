from django.core.management.base import BaseCommand
from surveys.tests.factories import basic_survey_structure, tight_survey_structure


class Command(BaseCommand):
    help = "Create sample surveys."

    # def add_arguments(self, parser):
    #     parser.add_argument('sample', nargs='+')

    def handle(self, *args, **options):
        basic_survey_structure("Long Text Survey")
        tight_survey_structure("Tight Structure Survey")
        self.stdout.write(self.style.SUCCESS("Done"))
