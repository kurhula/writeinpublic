from django.core.management.base import BaseCommand
from nuntium.tests.fixtures import popit_data

class Command(BaseCommand):
    def handle(self, *args, **options):
        print(popit_data.default[0]['name'])
