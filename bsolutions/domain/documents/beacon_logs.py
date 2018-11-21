import mongoengine
import factory
import factory.mongoengine
import factory.fuzzy

from bsolutions.domain.models.beacon import getCoordinate
from bsolutions.domain.models.profile import DOCUMENTOS_IDS, GENEROS_IDS


class EmbeddedUser(mongoengine.EmbeddedDocument):
    idUser = mongoengine.IntField(null=False)
    user = mongoengine.StringField()
    nombre = mongoengine.StringField()
    correo = mongoengine.EmailField()
    documento = mongoengine.StringField()
    tipoDocumento = mongoengine.IntField()
    direccion = mongoengine.StringField()
    telefono = mongoengine.StringField()


class EmbeddedProducto(mongoengine.EmbeddedDocument):
    idProducto = mongoengine.IntField(null=False)
    nombre = mongoengine.StringField()
    referencia = mongoengine.StringField()
    precio = mongoengine.FloatField()
    costo = mongoengine.FloatField()
    tipoProducto = mongoengine.IntField()


class EmbeddedInteraccion(mongoengine.EmbeddedDocument):
    idInteraccion = mongoengine.IntField(null=False)
    user = mongoengine.EmbeddedDocumentField(EmbeddedUser, default=EmbeddedUser())
    producto = mongoengine.EmbeddedDocumentField(EmbeddedProducto, default=EmbeddedProducto())


class EmbeddedBeaconPayload(mongoengine.EmbeddedDocument):
    geolocalizacion = mongoengine.StringField()
    bluetoothName = mongoengine.StringField()
    mensaje = mongoengine.StringField()
    UUID = mongoengine.StringField()
    bateria = mongoengine.IntField()
    interval = mongoengine.IntField()


class BeaconLogsDocument(mongoengine.Document):
    idBeacon = mongoengine.IntField(null=False)
    interaccion = mongoengine.EmbeddedDocumentField(EmbeddedInteraccion, default=EmbeddedInteraccion())
    payload = mongoengine.EmbeddedDocumentField(EmbeddedBeaconPayload, default=EmbeddedBeaconPayload())


class EmbeddedUserFactory(factory.mongoengine.MongoEngineFactory):

    class Meta:
        model = EmbeddedUser

    idUser = factory.fuzzy.FuzzyInteger(1, 100000)
    user = factory.Faker('user_name')
    nombre = factory.Faker('name')
    correo = factory.Faker('email')
    documento = factory.Faker('itin')
    tipoDocumento = factory.fuzzy.FuzzyChoice(DOCUMENTOS_IDS)
    direccion = factory.Faker('address')
    telefono = factory.Faker('msisdn')


class EmbeddedProductoFactory(factory.mongoengine.MongoEngineFactory):

    class Meta:
        model = EmbeddedProducto

    idProducto = factory.fuzzy.FuzzyInteger(1, 10000)
    nombre = factory.Faker('name')
    referencia = factory.Faker('email')
    precio = factory.fuzzy.FuzzyFloat(1, precision=2)
    costo = factory.fuzzy.FuzzyFloat(1, precision=2)
    tipoProducto = factory.fuzzy.FuzzyInteger(1, 1000)


class EmbeddedInteraccionFactory(factory.mongoengine.MongoEngineFactory):

    class Meta:
        model = EmbeddedInteraccion

    idInteraccion = factory.fuzzy.FuzzyInteger(1, 10000)
    user = factory.SubFactory(EmbeddedUserFactory)
    producto = factory.SubFactory(EmbeddedProductoFactory)


class EmbeddedBeaconPayloadFactory(factory.mongoengine.MongoEngineFactory):

    class Meta:
        model = EmbeddedBeaconPayload
        exclude = ('_UUID',)

    __UUID = factory.Faker('uuid4')

    geolocalizacion = factory.LazyAttribute(lambda n: getCoordinate())
    bluetoothName = factory.Faker('name')
    mensaje = factory.Faker('email')
    UUID = factory.LazyAttribute(lambda p: '{}'.format(p.__UUID))
    bateria = factory.fuzzy.FuzzyInteger(1, 100)
    interval = factory.fuzzy.FuzzyInteger(1, 10000)


class BeaconLogsDocumentFactory(factory.mongoengine.MongoEngineFactory):

    class Meta:
        model = BeaconLogsDocument

    idBeacon = factory.fuzzy.FuzzyInteger(1, 1000)
    interaccion = factory.SubFactory(EmbeddedInteraccionFactory)
    payload = factory.SubFactory(EmbeddedBeaconPayloadFactory)

