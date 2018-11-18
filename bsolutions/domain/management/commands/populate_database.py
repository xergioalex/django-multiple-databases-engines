from django.core.management.base import BaseCommand

from bsolutions.domain.factoryboy_utils import DBAwareFactory
from bsolutions.domain.models.notifications import NotificacionFactory
from bsolutions.domain.models.purchase import CompraProductoFactory


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

        parser.add_argument(
            '--db',
            default='default',
            type=str,
            nargs='?',
            help='base de datos que se utilizara'
        )

    def handle(self, *args, **options):
        for i in range(options['iteraciones']):
            CompraProductoFactory()
            NotificacionFactory()
            if i % 10000 == 0:
                print(f"elementos creados iteracion # {i}")
