import uuid

import factory
import factory.fuzzy
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel

from bsolutions.domain.models.beacon import getCoordinate
from bsolutions.domain.models.profile import GENEROS_IDS


class BeaconLogs(DjangoCassandraModel):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    beaconId = columns.Integer(primary_key=True)
    interaccionUser = columns.Map(columns.Integer(), columns.Text())
    interaccionProducto = columns.Map(columns.Integer(), columns.Text())
    geolocalizacion = columns.Text()
    bluetoothName = columns.Text(index=True)
    mensaje = columns.Text()
    UUID = columns.UUID(default=uuid.uuid4)
    bateria = columns.Integer(index=True)
    interval = columns.Integer()

    class Meta:
        get_pk_field = 'id'


class SocialUserMedia(DjangoCassandraModel):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    userId = columns.Integer(primary_key=True)
    address = columns.Text(index=True)
    age_range = columns.Text(index=True)
    birthday = columns.DateTime()
    context = columns.Text()
    cover = columns.Text()
    profile_pic = columns.Text()
    email = columns.Text()
    employee_number = columns.Integer(index=True)
    gender = columns.Text()
    hometown = columns.Text()
    languages = columns.List(columns.Text())
    location = columns.Text()
    religion = columns.Text()
    sports = columns.List(columns.Text())

    class Meta:
        get_pk_field = 'id'


class BeaconLogsCassandraFactory(factory.Factory):

    class Meta:
        model = BeaconLogs
        exclude = ('userId', 'userName')

    id = factory.Faker('uuid4')
    beaconId = factory.fuzzy.FuzzyInteger(1, 10000)
    userId = factory.fuzzy.FuzzyInteger(1, 100000)
    userName = factory.Faker('name')
    productoId = factory.fuzzy.FuzzyInteger(1, 10000)
    productoName = factory.Faker('name')
    interaccionUser = factory.LazyAttribute(lambda n: {n.userId: n.userName})
    interaccionProducto = factory.LazyAttribute(lambda n:  {n.productoId: n.productoName})
    geolocalizacion = factory.LazyAttribute(lambda n: getCoordinate())
    bluetoothName = factory.Faker('name')
    mensaje = factory.Faker('text')
    UUID = factory.Faker('uuid4')
    bateria = factory.fuzzy.FuzzyInteger(1, 100)
    interval = factory.fuzzy.FuzzyInteger(1, 10000)


class SocialUserMediaCassandraFactory(factory.Factory):

    class Meta:
        model = SocialUserMedia
        exclude = ('userId', 'userName')

    id = factory.Faker('uuid4')
    userId = factory.fuzzy.FuzzyInteger(1, 10000)
    address = factory.Faker('address')
    age_range = factory.Faker('year')
    birthday = factory.Faker('date_of_birth')
    context = factory.Faker('text')
    cover = factory.Faker('file_path')
    profile_pic = factory.Faker('file_path')
    email = factory.Faker('email')
    employee_number = factory.fuzzy.FuzzyInteger(1, 100000)
    gender = factory.fuzzy.FuzzyChoice(GENEROS_IDS)
    hometown = factory.Faker('city')
    languages = factory.Faker('sentences')
    location = factory.LazyAttribute(lambda n: getCoordinate())
    religion = factory.Faker('name')
    sports = factory.Faker('sentences')
