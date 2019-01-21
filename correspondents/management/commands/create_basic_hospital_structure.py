from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a hospital and departments."

    def add_arguments(self, parser):
        parser.add_argument('hospital_name')
        parser.add_argument('department_name')

    def handle(self, *args, **options):
        from correspondents.tests.factories import basic_hospital_structure
        basic_hospital_structure(hospital_name=options['hospital_name'], department_name=options['department_name'])
        self.stdout.write(self.style.SUCCESS('Done'))
