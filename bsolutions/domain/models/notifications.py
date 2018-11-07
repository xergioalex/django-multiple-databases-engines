from django.db import models


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
