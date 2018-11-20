import mongoengine


class EmbeddedUser(mongoengine.EmbeddedDocument):
    idUser = mongoengine.IntField(null=False)
    user = mongoengine.StringField()
    nombre = mongoengine.StringField()
    correo = mongoengine.EmailField()
    documento = mongoengine.StringField()
    tipoDocumento = mongoengine.IntField()
    direccion = mongoengine.StringField()
    telefono = mongoengine.StringField()


class EmbeddedProducto(mongoengine.Document):
    idProducto = mongoengine.IntField(null=False)
    nombre = mongoengine.StringField()
    referencia = mongoengine.StringField()
    precio = mongoengine.FloatField()
    tipoProducto = mongoengine.IntField()


class EmbeddedInteraccion(mongoengine.EmbeddedDocument):
    idInteraccion = mongoengine.IntField(null=False)
    user = mongoengine.EmbeddedDocumentField(EmbeddedUser, default=EmbeddedUser())
    producto = mongoengine.EmbeddedDocumentField(EmbeddedProducto, default=EmbeddedUser())


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
