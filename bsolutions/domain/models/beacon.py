from django.db import models

class Beacon(models.Model):
    nombre = models.CharField(max_length=45)
    referencia = models.CharField(max_length=45)
    modelo = models.CharField(max_length=45)
    ubicacion = models.CharField(max_length=45)

    class Meta:
        verbose_name_plural = "beacons"

    def __str__(self):
        return '%s' % (self.nombre)
