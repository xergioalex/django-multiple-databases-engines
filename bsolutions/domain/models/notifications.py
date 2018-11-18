from django.db import models

import factory
import factory.django
import factory.fuzzy

from .beacon import BeaconFactory
from .product import ProductoFactory


class Notificacion(models.Model):
    # notifications
    id = models.AutoField(primary_key=True)
    producto = models.ForeignKey('Producto', db_column='idProducto', on_delete=models.CASCADE, null=True)
    beacon = models.ForeignKey('Beacon', db_column='idBeacon', on_delete=models.CASCADE, null=False)
    mensaje = models.TextField(null=False)

    class Meta:
        db_table = "notificacion"
        verbose_name_plural = "notifications"

    def __str__(self):
        return '%s' % self.mensaje


class NotificacionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notificacion
        django_get_or_create = ('id',)

    id = factory.fuzzy.FuzzyInteger(1, 100000)
    mensaje = factory.Faker('text', max_nb_chars=100)
    producto = factory.SubFactory(ProductoFactory)
    beacon = factory.SubFactory(BeaconFactory)
