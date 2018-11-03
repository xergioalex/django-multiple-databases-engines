from django.db import models


class Compra(models.Model):
    cliente = models.ForeignKey('Cliente', db_column='idCliente', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', db_column='idProducto', on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    descuento = models.FloatField(default=0.0)
    medioPago = models.IntegerField()

    class Meta:
        verbose_name_plural = "products"

    def __str__(self):
        return '%s' % (self.cantidad)
