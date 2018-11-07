from django.db import models

import factory
import factory.django
import factory.fuzzy

from .notifications import NotificacionFactory
from .profile import ClienteFactory


class Interaccion(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey('Cliente', db_column='idCliente', on_delete=models.CASCADE, null=False)
    notificacion = models.ForeignKey('Notificacion', db_column='idNotificacion', on_delete=models.CASCADE, null=False)
    fecha = models.DateTimeField(auto_now_add=True, null=False)
    materializado = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = "interaccion"
        verbose_name_plural = "beacons"

    def __str__(self):
        return '%s' % (self.fecha)


class InteraccionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Interaccion

    cliente = factory.SubFactory(ClienteFactory)
    notificacion = factory.SubFactory(NotificacionFactory)
    fecha = factory.Faker('date_time_this_year')
    materializado = factory.Faker('boolean')
