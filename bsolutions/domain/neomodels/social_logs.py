from datetime import datetime

from django_neomodel import DjangoNode
from neomodel import StructuredRel, StringProperty, DateTimeProperty, UniqueIdProperty


class InteraccionNode(StructuredRel):
    fecha = DateTimeProperty(default=datetime.utcnow)
    mensaje = StringProperty()

    class Meta:
        app_label = 'logs'


class BeaconNode(DjangoNode):
    uid = UniqueIdProperty()
    creada = DateTimeProperty(default=datetime.utcnow)

    class Meta:
        app_label = 'logs'


class PersonaNode(DjangoNode):
    uid = UniqueIdProperty(unique_index=True)
    nombre = StringProperty()
    creada = DateTimeProperty(default=datetime.utcnow)

    class Meta:
        app_label = 'logs'
