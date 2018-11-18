from django.db import models
import factory
import factory.django
import factory.fuzzy


class Beacon(models.Model):
    id = models.AutoField(primary_key=True)
    referencia = models.CharField(max_length=45, null=False)
    modelo = models.CharField(max_length=45, null=False)
    ubicacion = models.CharField(max_length=45, null=False)

    class Meta:
        db_table = "beacon"
        verbose_name_plural = "beacons"

    def __str__(self):
        return '%s' % (self.referencia)


class BeaconFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Beacon
        django_get_or_create = ('id',)

    id = factory.fuzzy.FuzzyInteger(1, 1000)
    referencia = factory.Faker('itin')
    modelo = factory.Faker('zipcode')
    ubicacion = factory.Faker('geo_coordinate')
