import random
from faker import Factory as FakerFactory

from django.core.management.base import BaseCommand

from bsolutions.domain.neomodels.social_logs import BeaconNodeFactory, PersonaNodeFactory, PersonaNode, BeaconNode


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
            '--create_rel',
            default=False,
            type=bool,
            nargs='?',
            help='crear relaciones'
        )

    def handle(self, *args, **options):
        if options['create_rel']:

            faker = FakerFactory.create()
            i = 0
            limit = PersonaNode.nodes.has(beacons=False).__len__()

            for query in (PersonaNode.nodes.has(beacons=False)[x:x+10] for x in range(0, limit, 10)):
                random_limit = random.randint(1, 10)
                for persona_node in query:
                    for beacon_node in BeaconNode.nodes.order_by('?')[:random_limit]:
                        rel = persona_node.beacons.connect(beacon_node)
                        rel.mensaje = faker.text(max_nb_chars=200, ext_word_list=None)
                        rel.save()
                        i += 1
                        print(f"relaciones creadas {i}")

            return

        for _ in range(options['iteraciones']):
            BeaconNodeFactory().save()
            PersonaNodeFactory().save()

            if _ % 1000 == 0:
                print(f"elementos creados iteracion # {_}")
