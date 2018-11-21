import mongoengine
import factory
import factory.mongoengine
import factory.fuzzy

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
    UUID = mongoengine.UUIDField()
    bateria = mongoengine.IntField()
    interval = mongoengine.IntField()


class BeaconLogsDocument(mongoengine.Document):
    idBeacon = mongoengine.IntField(null=False)
    interaccion = mongoengine.EmbeddedDocumentField(EmbeddedInteraccion, default=EmbeddedInteraccion())
    payload = mongoengine.EmbeddedDocumentField(EmbeddedBeaconPayload, default=EmbeddedBeaconPayload())


class EmbeddedUserFactory(factory.Factory):
    FACTORY_FOR = EmbeddedUser

    idUser = factory.fuzzy.FuzzyInteger(1, 100000)
    nombre = factory.Faker('name')
    correo = factory.Faker('email')
    documento = factory.Faker('itin')
    tipoDocumento = factory.fuzzy.FuzzyChoice(DOCUMENTOS_IDS)
    genero = factory.fuzzy.FuzzyChoice(GENEROS_IDS)
    edad = factory.fuzzy.FuzzyInteger(1, 100)
    direccion = factory.Faker('address')
    telefono = factory.Faker('msisdn')


class EmbeddedProductoFactory(factory.Factory):
    FACTORY_FOR = EmbeddedProducto

    idProducto = factory.fuzzy.FuzzyInteger(1, 10000)
    nombre = factory.Faker('name')
    referencia = factory.Faker('email')
    precio = factory.fuzzy.FuzzyFloat(1, precision=2)
    costo = factory.fuzzy.FuzzyFloat(1, precision=2)
    tipoProducto = factory.fuzzy.FuzzyInteger(1, 1000)


class EmbeddedInteraccionFactory(mongoengine.EmbeddedDocument):
    FACTORY_FOR = EmbeddedInteraccion

    idInteraccion = factory.fuzzy.FuzzyInteger(1, 10000)
    user = factory.SubFactory(EmbeddedUserFactory)
    producto = factory.SubFactory(EmbeddedProductoFactory)


class EmbeddedBeaconPayloadFactory(factory.Factory):
    FACTORY_FOR = EmbeddedBeaconPayload

    geolocalizacion = factory.Faker('latlng')
    bluetoothName = factory.Faker('name')
    mensaje = factory.Faker('email')
    UUID = factory.Faker('uuid4')
    bateria = factory.fuzzy.FuzzyInteger(1, 100)
    interval = factory.fuzzy.FuzzyInteger(1, 10000)


class BeaconLogsDocumentFactory(factory.mongoengine.MongoEngineFactory):

    class Meta:
        model = BeaconLogsDocument

    idBeacon = mongoengine.IntField(null=False)
    interaccion = mongoengine.EmbeddedDocumentField(EmbeddedInteraccion, default=EmbeddedInteraccion())
    payload = mongoengine.EmbeddedDocumentField(EmbeddedBeaconPayload, default=EmbeddedBeaconPayload())

