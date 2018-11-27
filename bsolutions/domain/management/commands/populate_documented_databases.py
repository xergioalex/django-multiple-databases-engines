from django.core.management.base import BaseCommand

from bsolutions.domain.documents.beacon_logs import BeaconLogsDocumentFactory
from bsolutions.domain.factoryboy_utils import DBAwareFactory
from bsolutions.domain.models.notifications import NotificacionFactory
from bsolutions.domain.models.purchase import CompraProductoFactory
from config.settings.base import couchDBdatabase


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
            a = BeaconLogsDocumentFactory()
            b = a.to_mongo().to_dict()
            b['_id'] = str(b['_id'])
            b['collection'] = 'BeaconLogsDocument'
            couchDBdatabase.create_document(b)
            print(f"elementos creados iteracion # {_}")
