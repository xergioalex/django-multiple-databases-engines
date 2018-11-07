from django.db import models


class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45, null=False)
    referencia = models.CharField(max_length=45, null=False)
    precio = models.FloatField(null=False)
    tipoProducto = models.ForeignKey('TipoProducto', db_column='idTipoProducto', on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = "producto"
        verbose_name_plural = "products"

    def __str__(self):
        return '%s' % (self.nombre)
