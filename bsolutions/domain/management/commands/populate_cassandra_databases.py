from django.core.management.base import BaseCommand

from bsolutions.domain.models.cassandra_models import BeaconLogsCassandraFactory, SocialUserMediaCassandraFactory


class Command(BaseCommand):
    help = '--iteraciones para asignar un numero maximo de iteraciones'

    def add_arguments(self, parser):
        parser.add_argument(
            '--iteraciones',
            default=1000,
            type=int,
            nargs='?',
            help='numero de iteraciones'
        )

    def handle(self, *args, **options):
        for _ in range(options['iteraciones']):
            BeaconLogsCassandraFactory().save()
            SocialUserMediaCassandraFactory().save()
            if _ % 10000 == 0:
                print(f"elementos creados iteracion # {_}")
