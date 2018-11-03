from django.db import models

class Interaccion(models.Model):
    cliente = models.ForeignKey('Cliente', db_column='idCliente', on_delete=models.CASCADE)
    notificacion = models.ForeignKey('Notificacion', db_column='idNotificacion', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    Materializado = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "beacons"

    def __str__(self):
        return '%s' % (self.fecha)
