from django.db import models


class Compra(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey('Cliente', db_column='idCliente', on_delete=models.CASCADE, null=False)
    fecha = models.DateTimeField(auto_now_add=True, null=False)
    medioPago = models.IntegerField(null=False)
    descuento = models.FloatField(default=0.0, null=True)


    class Meta:
        db_table = "compra"
        verbose_name_plural = "products"

    def __str__(self):
        return '%s' % (self.cliente_id)


class CompraProducto(models.Model):
    id = models.AutoField(primary_key=True)
    compra = models.ForeignKey('Compra', db_column='idCompra', on_delete=models.CASCADE, null=False)
    producto = models.ForeignKey('Producto', db_column='idProducto', on_delete=models.CASCADE, null=False)
    cantidad = models.PositiveIntegerField(default=1, null=False)
    descuento = models.FloatField(default=0.0, null=True)

    class Meta:
        db_table = "compra_producto"
        verbose_name_plural = "products"

    def __str__(self):
        return '%s' % (self.cantidad)
