from django.db import models


class Notificacion(models.Model):
    # notifications
    producto = models.ForeignKey('Producto', db_column='idProducto', on_delete=models.CASCADE)
    beacon = models.ForeignKey('Beacon', db_column='idBeacon', on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "notifications"

    def __str__(self):
        return '%s' % self.mensaje
