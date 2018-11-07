from django.db import models
import factory
import factory.django


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

    referencia = factory.Faker('itin')
    modelo = factory.Faker('zipcode')
    ubicacion = factory.Faker('geo_coordinate')
