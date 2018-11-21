import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel


class BeaconLogs(DjangoCassandraModel):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    beaconId = columns.Integer()
    interaccionUser = columns.Map(columns.Integer(), columns.Text())
    interaccionProducto = columns.Map(columns.Integer(), columns.Text())
    geolocalizacion = columns.Text()
    bluetoothName = columns.Text()
    mensaje = columns.Text()
    UUID = columns.UUID(default=uuid.uuid4)
    bateria = columns.Integer()
    interval = columns.Integer()


class SocialUserMedia(DjangoCassandraModel):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    userId = columns.Integer()
    address = columns.Text()
    age_range = columns.Text()
    birthday = columns.DateTime()
    context = columns.Text()
    cover = columns.Text()
    profile_pic = columns.Text()
    email = columns.Text()
    employee_number = columns.Integer()
    gender = columns.Text()
    hometown = columns.Text()
    languages = columns.List(columns.Text())
    location = columns.Text()
    religion = columns.Text()
    sports = columns.List(columns.Text())
