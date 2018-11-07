from django.db import models


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

# class FooFactory(factory.Factory):
#     class Meta:
#         model = Foo
#
#     bar = factory.RelatedFactory(BarFactory)  # Not BarFactory()
