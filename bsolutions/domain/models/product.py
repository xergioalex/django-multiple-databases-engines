from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=45)
    referencia = models.CharField(max_length=45)
    precio = models.FloatField()
    tipoProducto = models.ForeignKey('TipoProducto', db_column='idTipoProducto', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "products"

    def __str__(self):
        return '%s' % (self.nombre)
