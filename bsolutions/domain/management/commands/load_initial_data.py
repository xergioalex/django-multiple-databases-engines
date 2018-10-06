from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    def handle(self, **options):
        file_prefix = "/app/beyond_campus/domain/fixtures/local/"
        call_command('loaddata', file_prefix + "01.initial_data_landlords.json", verbosity=0)
